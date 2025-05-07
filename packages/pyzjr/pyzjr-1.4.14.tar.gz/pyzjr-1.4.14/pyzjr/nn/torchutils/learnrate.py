# 学习率动态调整
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from pyzjr.nn.torchutils.lr_scheduler import _LRScheduler
import pyzjr.Z as Z
from pyzjr.utils.mathfun import cos

__all__ = [
           # 项目常用的两种
           "get_optimizer",
           # 复现 https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate torch官方实现
           "FixedStepLR",
           "MultiStepLR",
           "CosineAnnealingLR",
           "WarmUpLR",
            # 继承了torch.optim.lr_scheduler的_LRScheduler
           "WarmUp",
           "FindLR",
            # 小工具：用于学习率范围测试
           "lr_finder",]

def get_optimizer(model, optimizer_type='adam', init_lr=0.001, momentum=None, weight_decay=None):
    """
    根据指定的优化器类型返回相应的优化器对象，并根据批次大小调整初始学习率。

    :param model: 要优化的神经网络模型
    :param optimizer_type: 优化器类型，可以是 'adam'、'sgd'、'adamw'，默认为 'adam'
    :param init_lr: 初始学习率，默认为 0.001
    :param momentum: SGD优化器的动量参数，默认为 None
    :param weight_decay: 权重衰减（L2正则化）参数，默认为 None
    :return: 优化器对象
    """
    if optimizer_type in ['adam', 'Adam']:
        optimizer = optim.Adam(model.parameters(), lr=init_lr, betas=(momentum or 0.9, 0.999),
                               weight_decay=(weight_decay or 1e-4))
    elif optimizer_type in ['sgd', 'SGD']:
        optimizer = optim.SGD(model.parameters(), lr=init_lr, momentum=(momentum or 0.9), nesterov=True,
                              weight_decay=(weight_decay or 1e-4))
    elif optimizer_type in ['adamw', 'AdamW']:
        optimizer = optim.AdamW(model.parameters(), lr=init_lr, betas=(momentum or 0.9, 0.999),
                                weight_decay=weight_decay or 1e-2, eps=1e-8)
    else:
        raise ValueError("Unsupported optimizer type:: {}".format(optimizer_type))

    return optimizer

class FindLR(_LRScheduler):
    """
    exponentially increasing learning rate

    Args:
        optimizer: optimzier(e.g. SGD)
        num_iter: totoal_iters
        max_lr: maximum  learning rate
    """
    def __init__(self, optimizer, max_lr=10, num_iter=100, last_epoch=-1):

        self.total_iters = num_iter
        self.max_lr = max_lr
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        return [base_lr * (self.max_lr / base_lr) ** (self.last_epoch / (self.total_iters + 1e-32)) for base_lr in self.base_lrs]


class lr_finder():
    def __init__(self,net, dataloader, loss_function, optimizer_type="sgd",num_iter=100,batch_size=4):
        self.net = net
        self.dataloader = dataloader
        self.loss_function = loss_function
        self.optimizer_type = optimizer_type
        self.num_iter = num_iter
        self.batch_size = batch_size

    def update(self, init_lr=1e-7, max_lr=10):
        n = 0
        learning_rate = []
        losses = []
        optimizer = get_optimizer(self.net, self.optimizer_type, init_lr)
        lr_scheduler = FindLR(optimizer, max_lr=max_lr, num_iter=self.num_iter)
        epoches = int(self.num_iter / len(self.dataloader)) + 1

        for epoch in range(epoches):
            self.net.train()
            for batch_index, (images, labels) in enumerate(self.dataloader):
                if n > self.num_iter:
                    break
                if torch.cuda.is_available():
                    images = images.cuda()
                    labels = labels.cuda()

                optimizer.zero_grad()
                predicts = self.net(images)
                loss = self.loss_function(predicts, labels)
                if torch.isnan(loss).any():
                    n += 1e8
                    break
                loss.backward()
                optimizer.step()
                lr_scheduler.step()

                print('Iterations: {iter_num} [{trained_samples}/{total_samples}]\tLoss: {:0.4f}\tLR: {:0.8f}'.format(
                    loss.item(),
                    optimizer.param_groups[0]['lr'],
                    iter_num=n,
                    trained_samples=batch_index * self.batch_size + len(images),
                    total_samples=len(self.dataloader),
                ))

                learning_rate.append(optimizer.param_groups[0]['lr'])
                losses.append(loss.item())
                n += 1

        self.learning_rate = learning_rate[10:-5]
        self.losses = losses[10:-5]

    def plotshow(self, show=True):
        import matplotlib
        matplotlib.use("TkAgg")
        fig, ax = plt.subplots(1, 1)
        ax.plot(self.learning_rate, self.losses)
        ax.set_xlabel('learning rate')
        ax.set_ylabel('losses')
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0e'))
        if show:
            plt.show()

    def save(self, path='result.jpg'):
        self.plotshow(show=False)
        plt.savefig(path)

class FixedStepLR:
    """
    Compared with Torch's official StepLR and completed the functional implementation.
    每 step_size 个周期通过 gamma 衰减每个参数组的学习率。
    """
    def __init__(self, optimizer, step_size, gamma=0.1):
        self.optimizer = optimizer
        self.step_size = step_size
        self.gamma = gamma
        self.last_epoch = 0

    def get_lr(self):
        if self.last_epoch == 0 or (self.last_epoch % self.step_size != 0):
            return [group['lr'] for group in self.optimizer.param_groups]
        else:
            return [lr * self.gamma for lr in [group['lr'] for group in self.optimizer.param_groups]]

    def step(self):
        self.last_epoch += 1
        new_lr = self.get_lr()
        for param_group, lr in zip(self.optimizer.param_groups, new_lr):
            param_group['lr'] = lr


class MultiStepLR:
    """
    Compared with Torch's official MultiStepLR and completed the functional implementation.
    当达到里程碑之一, 将每个参数组的学习率衰减 gamma.
    """
    def __init__(self, optimizer, milestones, gamma=0.1):
        self.optimizer = optimizer
        self.milestones = self.to_constant(milestones)
        self.gamma = gamma
        self.last_epoch = 0

    def to_constant(self, x):
        if isinstance(x, list):
            return [int(element) for element in x]

    def get_lr(self):
        import bisect
        milestone_index = bisect.bisect_right(self.milestones, self.last_epoch)
        if self.last_epoch not in self.milestones:
            return [group['lr'] for group in self.optimizer.param_groups]
        else:
            return [group['lr'] * self.gamma ** milestone_index
                    for group in self.optimizer.param_groups]

    def step(self):
        self.last_epoch += 1
        new_lr = self.get_lr()
        for param_group, lr in zip(self.optimizer.param_groups, new_lr):
            param_group['lr'] = lr

class CosineAnnealingLR:
    def __init__(self, optimizer, T_max, eta_min=0):
        self.optimizer = optimizer
        self.T_max = T_max
        self.eta_min = eta_min
        self.last_epoch = 0
        if self.last_epoch == 0:
            for group in optimizer.param_groups:
                group.setdefault('initial_lr', group['lr'])
        self.base_lrs = list(map(lambda group: group['initial_lr'], optimizer.param_groups))

    def get_lr(self):
        if self.last_epoch == 0:
            return self.base_lrs
        elif (self.last_epoch - 1 - self.T_max) % (2 * self.T_max) == 0:
            return [group['lr'] + (base_lr - self.eta_min) *
                    (1 - cos(Z.pi / self.T_max)) / 2
                    for base_lr, group in zip(self.base_lrs, self.optimizer.param_groups)]

        return [(1 + cos(Z.pi * self.last_epoch / self.T_max)) /
                (1 + cos(Z.pi * (self.last_epoch - 1) / self.T_max)) *
                (group['lr'] - self.eta_min) + self.eta_min
                for group in self.optimizer.param_groups]

    def step(self):
        self.last_epoch += 1
        new_lr = self.get_lr()
        for param_group, lr in zip(self.optimizer.param_groups, new_lr):
            param_group['lr'] = lr

class WarmUp(_LRScheduler):
    """
    warmup_training learning rate scheduler
    Args:
        optimizer: optimzier
        total_iters: totoal_iters of warmup phase
    """
    def __init__(self, optimizer, total_iters, last_epoch=-1):
        self.total_iters = total_iters
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        """we will use the first m batches, and set the learning
        rate to base_lr * m / total_iters
        """
        return [base_lr * self.last_epoch / (self.total_iters + 1e-8) for base_lr in self.base_lrs]

class WarmUpLR:
    def __init__(self, optimizer, train_loader, epochs, warmup_epochs=1, warmup_factor=1e-3,):
        """
        :param optimizer: 优化器对象，用于更新模型参数。
        :param train_loader: 训练的数据加载器
        :param epochs: 总训练周期数。
        :param warmup_epochs: 学习率预热的周期数。仅在 warmup 为 True 时有效。默认为 1。
        :param warmup_factor: 学习率预热的初始倍率因子。仅在 warmup 为 True 时有效。默认为 1e-3。
        """
        self.optimizer = optimizer
        self.warmup_epochs = warmup_epochs
        self.epochs = epochs
        self.num_step = len(train_loader) * self.epochs   # num_step训练步数总数，通常等于 len(train_loader) * epochs。
        self.warmup_factor = warmup_factor
        self.scheduler = self.get_scheduler()

    def get_scheduler(self):
        def f(x):
            """
            根据step数返回一个学习率倍率因子，
            """
            if self.warmup_epochs > 0 and x <= (self.warmup_epochs * self.num_step):
                alpha = float(x) / (self.warmup_epochs * self.num_step)
                return self.warmup_factor * (1 - alpha) + alpha
            else:
                # warmup后lr倍率因子从1 -> 0
                # 参考deeplab_v2: Learning rate policy
                return (1 - (x - self.warmup_epochs * self.num_step) / ((self.epochs - self.warmup_epochs) * self.num_step)) ** 0.9
        return optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda=f)

    def step(self):
        self.scheduler.step()

    def get_lr(self):
        return [group['lr'] for group in self.optimizer.param_groups]

if __name__=="__main__":
    from torch.optim import lr_scheduler

    class SimpleModel(torch.nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.linear = torch.nn.Linear(1, 1)

        def forward(self, x):
            return self.linear(x)

    x_data = torch.tensor([[1.0], [2.0], [3.0]])
    y_data = torch.tensor([[2.0], [4.0], [6.0]])

    model = SimpleModel()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    criterion = torch.nn.MSELoss()
    # 固定的步数gamma衰减测试
    # scheduler = lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
    # scheduler = FixedStepLR(optimizer, step_size=30, gamma=0.1)
    # 当达到里程碑时进行gamma衰减测试
    # scheduler = lr_scheduler.MultiStepLR(optimizer, milestones=[30, 80], gamma= 0.1)
    # scheduler = MultiStepLR(optimizer, milestones=[30, 80], gamma=0.1)
    # scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=25)
    scheduler = WarmUpLR(optimizer, num_step=100, epochs=100)
    # scheduler = lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=25, T_mult=1, eta_min=0)
    epochs = 100
    for epoch in range(epochs):
        y_pred = model(x_data)
        loss = criterion(y_pred, y_data)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        scheduler.step()
        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}, Learning Rate: {optimizer.param_groups[0]["lr"]}')

    with torch.no_grad():
        test_data = torch.tensor([[4.0]])
        predicted_y = model(test_data)
        print(f'After training, input 4.0, predicted output: {predicted_y.item()}')
