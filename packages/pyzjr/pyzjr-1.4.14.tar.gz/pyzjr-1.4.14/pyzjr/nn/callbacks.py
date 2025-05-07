import os
import torch
from collections import defaultdict, deque
import time
import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import scipy.signal as signal
from torch.utils.tensorboard import SummaryWriter

from pyzjr.visualize.printf import LoadingBar

__all__ = ["AverageMeter", "SmoothedValue", "MetricLogger", "ConfusionMatrixRecord",
           "LossHistory", "ErrorRateMonitor", "ProcessMonitor"]

class AverageMeter(object):
    """A simple class that maintains the running average of a quantity

    Example:
    ```
        loss_avg = AverageMeter()
        loss_avg.update(2)
        loss_avg.update(4)
        loss_avg() = 3
    ```
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

class SmoothedValue(object):
    """Track a series of values and provide access to smoothed values over a
    window or the global series average.
    """
    def __init__(self, window_size=20, fmt=None):
        if fmt is None:
            fmt = "{value:.4f} ({global_avg:.4f})"
        self.deque = deque(maxlen=window_size)
        self.total = 0.0
        self.count = 0
        self.fmt = fmt

    def update(self, value, n=1):
        self.deque.append(value)
        self.count += n
        self.total += value * n

    @property
    def median(self):
        d = torch.tensor(list(self.deque))
        return d.median().item()

    @property
    def avg(self):
        d = torch.tensor(list(self.deque), dtype=torch.float32)
        return d.mean().item()

    @property
    def global_avg(self):
        return self.total / self.count

    @property
    def max(self):
        return max(self.deque)

    @property
    def value(self):
        return self.deque[-1]

    def __str__(self):
        return self.fmt.format(
            median=self.median,
            avg=self.avg,
            global_avg=self.global_avg,
            max=self.max,
            value=self.value)

class MetricLogger(object):
    def __init__(self, delimiter="\t", load_bar = False):
        self.meters = defaultdict(SmoothedValue)
        self.delimiter = delimiter

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, torch.Tensor):
                v = v.item()
            assert isinstance(v, (float, int))
            self.meters[k].update(v)

    def __getattr__(self, attr):
        if attr in self.meters:
            return self.meters[attr]
        if attr in self.__dict__:
            return self.__dict__[attr]
        raise AttributeError("'{}' object has no attribute '{}'".format(
            type(self).__name__, attr))

    def __str__(self):
        loss_str = []
        for name, meter in self.meters.items():
            loss_str.append(
                "{}: {}".format(name, str(meter))
            )
        return self.delimiter.join(loss_str)

    def add_meter(self, name, meter):
        self.meters[name] = meter

    def log_every(self, iterable, print_freq, header=None):
        i = 0
        if not header:
            header = ''
        start_time = time.time()
        end = time.time()
        iter_time = SmoothedValue(fmt='{avg:.4f}')
        data_time = SmoothedValue(fmt='{avg:.4f}')
        space_fmt = ':' + str(len(str(len(iterable)))) + 'd'

        load_bar = LoadingBar(20)

        if torch.cuda.is_available():
            log_msg = self.delimiter.join([
                header,
                '[{0' + space_fmt + '}/{1}]',
                'Process: {Process}',
                'eta: {eta}',
                '{meters}',
                'time: {time}',
                'data: {data}',
                'max mem: {memory:.0f}'
            ])
        else:
            log_msg = self.delimiter.join([
                header,
                '[{0' + space_fmt + '}/{1}]',
                'Process: {Process}',
                'eta: {eta}',
                '{meters}',
                'time: {time}',
                'data: {data}'
            ])
        MB = 1024.0 * 1024.0

        for obj in iterable:
            data_time.update(time.time() - end)
            yield obj
            iter_time.update(time.time() - end)
            if i % print_freq == 0:
                eta_seconds = iter_time.global_avg * (len(iterable) - i)
                eta_string = str(datetime.timedelta(seconds=int(eta_seconds)))
                if torch.cuda.is_available():
                    progress = (i + 1) / len(iterable)
                    bar_string = load_bar(progress)
                    print("\r", log_msg.format(
                        i,
                        len(iterable),
                        Process=bar_string,
                        eta=eta_string,
                        meters=str(self),
                        time=str(iter_time), data=str(data_time),
                        memory=torch.cuda.max_memory_allocated() / MB), end=' ', flush=True)
                else:
                    progress = (i + 1) / len(iterable)
                    bar_string = load_bar(progress)
                    print("\r", log_msg.format(
                        i, bar_string,
                        len(iterable),
                        eta=eta_string,
                        meters=str(self),
                        time=str(iter_time), data=str(data_time)), end=' ', flush=True)
            i += 1
            end = time.time()
        total_time = time.time() - start_time
        total_time_str = str(datetime.timedelta(seconds=int(total_time)))
        print("\n", f'{header} Total time: {total_time_str}')

class ConfusionMatrixRecord(object):
    """For details:https://blog.csdn.net/m0_62919535/article/details/132893016"""
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.mat = None

    # def update(self, true, pred):
    #     t, p = true.flatten(), pred.flatten()
    #     n = self.num_classes
    #     if self.mat is None:
    #         self.mat = torch.zeros((n, n), dtype=torch.int64, device=t.device)
    #     with torch.no_grad():
    #         k = (t >= 0) & (t < n)
    #         inds = n * t[k].to(torch.int64) + p[k]
    #         self.mat += torch.bincount(inds, minlength=n**2).reshape(n, n)
    def update(self, true, pred):
        t, p = true.flatten(), pred.flatten()
        n = self.num_classes
        if self.mat is None:
            self.mat = torch.zeros((n, n), dtype=torch.int64, device=t.device)
        for i in range(self.num_classes):
            for j in range(self.num_classes):
                self.mat[i, j] += torch.sum((t == i) & (p == j))


    def reset(self):
        if self.mat is not None:
            self.mat.zero_()

    @property
    def ravel(self):
        """
        计算混淆矩阵的TN, FP, FN, TP
        支持二分类和多分类
        """
        h = self.mat.float()
        n = self.num_classes
        if n == 2:
            TP, FN, FP, TN = h.flatten()
            return TP, FN, FP, TN
        if n > 2:
            TP = h.diag()
            FN = h.sum(dim=1) - TP
            FP = h.sum(dim=0) - TP
            TN = torch.sum(h) - (torch.sum(h, dim=0) + torch.sum(h, dim=1) - TP)

            return TP, FN, FP, TN

    def compute(self, eps = 1e-6):
        """
        主要在eval的时候使用,可以调用ravel获得TN, FP, FN, TP, 进行其他指标的计算
        计算全局预测准确率(混淆矩阵的对角线为预测正确的个数)
        计算每个类别的准确率
        计算每个类别预测与真实目标的iou,IoU = TP / (TP + FP + FN)
        """
        h = self.mat.float()
        # 全局准确率
        acc_global = torch.diag(h).sum() / (h.sum() + eps)
        # 类别准确率
        acc = torch.diag(h) / (h.sum(dim=1) + eps)
        # IoU
        iu = torch.diag(h) / (h.sum(dim=1) + h.sum(dim=0) - torch.diag(h) + eps)
        return acc_global, acc, iu

    def __str__(self):
        acc_global, acc, iu = self.compute()
        return (
            'global correct: {:.1f}\n'
            'average row correct: {}\n'
            'IoU: {}\n'
            'mean IoU: {:.1f}').format(
            acc_global.item() * 100,
            ['{:.1f}'.format(i) for i in (acc * 100).tolist()],
            ['{:.1f}'.format(i) for i in (iu * 100).tolist()],
            iu.mean().item() * 100)


class LossHistory():
    def __init__(self, log_dir, model, input_shape):
        self.log_dir = log_dir
        self.losses = []
        self.val_loss = []

        os.makedirs(self.log_dir, exist_ok=True)
        self.writer = SummaryWriter(self.log_dir)
        try:
            device = 'cpu'
            dummy_input = torch.randn(2, 3, input_shape[0], input_shape[1]).to(device)
            self.writer.add_graph(model.to(device), dummy_input)
        except:
            pass

    def append_loss(self, epoch, loss, val_loss):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self.losses.append(loss)
        self.val_loss.append(val_loss)

        with open(os.path.join(self.log_dir, "epoch_loss.txt"), 'a') as f:
            f.write(f"Epoch {epoch}: train: {loss} val: {val_loss}")
            f.write("\n")

        self.writer.add_scalar('loss', loss, epoch)
        self.writer.add_scalar('val_loss', val_loss, epoch)
        self.loss_plot()

    def loss_plot(self):
        iters = range(len(self.losses))
        losses_cpu = torch.tensor(self.losses).cpu().numpy()
        val_loss_cpu = torch.tensor(self.val_loss).cpu().numpy()

        plt.figure()
        plt.plot(iters, losses_cpu, 'red', linewidth=2, label='train loss')
        plt.plot(iters, val_loss_cpu, 'coral', linewidth=2, label='val loss')

        try:
            if len(self.losses) < 25:
                num = 5
            else:
                num = 15
            smoothed_train_loss = signal.savgol_filter(losses_cpu, num, 3)
            smoothed_val_loss = signal.savgol_filter(val_loss_cpu, num, 3)

            plt.plot(iters, smoothed_train_loss, 'green', linestyle='--', linewidth=2, label='smooth train loss')
            plt.plot(iters, smoothed_val_loss, '#8B4513', linestyle='--', linewidth=2, label='smooth val loss')
        except:
            pass

        plt.grid(True)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend(loc="upper right")
        plt.savefig(os.path.join(self.log_dir, "epoch_loss.png"))

        plt.cla()
        plt.close("all")

    def close(self):
        self.writer.close()

class ErrorRateMonitor:
    """
    错误率监视器,传入train和val的准确率,记录错误率,仅用于分类任务
    """
    def __init__(self, log_dir):
        self.save_path = os.path.join(log_dir, "Error_rate.png")
        self.fig, self.ax = plt.subplots()
        self.train_error_rates = []
        self.val_error_rates = []
        self.acc_log_path = os.path.join(log_dir, "acc_log.txt")
        self.ax.set_xlabel('Epoch')
        self.ax.set_ylabel('Error_rate')

    def append_acc(self, epoch, train_acc, val_acc):
        train_error_rate = 1 - train_acc
        val_error_rate = 1 - val_acc

        self.train_error_rates.append(train_error_rate)
        self.val_error_rates.append(val_error_rate)

        plt.title(f'Epoch {epoch}')
        with open(self.acc_log_path, 'a') as acc_file:
            acc_file.write(
                f"Epoch {epoch}: Train Accuracy: {train_acc:.4f}, Validation Accuracy: {val_acc:.4f}\n")
        self.error_plot(epoch)

    def error_plot(self, epoch):
        iters = np.arange(1, epoch + 1)

        self.ax.clear()
        self.ax.plot(iters, self.train_error_rates[:len(iters)], 'red', linewidth=2, label='train error')
        self.ax.plot(iters, self.val_error_rates[:len(iters)], 'coral', linewidth=2, label='val error')
        try:
            if len(self.train_error_rates) < 25:
                num = 5
            else:
                num = 15

            self.ax.plot(iters, signal.savgol_filter(self.train_error_rates[:len(iters)], num, 3), 'green',
                         linestyle='--',
                         linewidth=2, label='smooth train error')
            self.ax.plot(iters, signal.savgol_filter(self.val_error_rates[:len(iters)], num, 3), '#8B4513',
                         linestyle='--',
                         linewidth=2, label='smooth val error')
        except:
            pass

        self.ax.grid(True)
        self.ax.legend(loc="upper right")

        self.fig.savefig(self.save_path)

    def close(self):
        plt.close("all")


class ProcessMonitor:
    def __init__(self, epochs, metric='train_loss', mode='min',
                 save_path='./logs', figsize=(8, 6)):
        self.figsize = figsize
        self.save_path = os.path.join(save_path, f'{metric}.png')
        self.metric_name = metric
        self.metric_mode = mode
        self.epochs = epochs
        self.history = {}
        self.step, self.epoch = 0, 0

        self.csv_filename = os.path.join(save_path, f'{metric}.csv')
        os.makedirs(save_path, exist_ok=True)
        self._init_csv()

    def _init_csv(self):
        """初始化 CSV 文件，如果文件不存在，则创建一个包含列标题的空文件"""
        if not os.path.exists(self.csv_filename):
            columns = ['epoch', self.metric_name, 'train_loss', 'val_loss']
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.csv_filename, index=False)

    def start(self):
        print('\nView dynamic loss/metric plot: \n' + os.path.abspath(self.save_path))
        x_bounds = [0, min(10, self.epochs)]
        title = f'best {self.metric_name} = ?'
        self.update_graph(title=title, x_bounds=x_bounds)

    def log_epoch(self, info):
        self.epoch += 1
        info['epoch'] = self.epoch

        # 更新历史记录字典
        for name, metric in info.items():
            if name not in self.history:
                self.history[name] = []
            self.history[name].append(metric)

        # 使用 pandas 更新 CSV 文件
        self._save_to_csv()

        dfhistory = pd.DataFrame(self.history)
        n = len(dfhistory)
        x_bounds = [dfhistory['epoch'].min(), min(10 + (n // 10) * 10, self.epochs)]
        title = self.get_title()
        self.step, self.batchs = 0, self.step
        self.update_graph(title=title, x_bounds=x_bounds)

    def _save_to_csv(self):
        """将当前历史记录保存到 CSV 文件"""
        df = pd.DataFrame(self.history)
        df.to_csv(self.csv_filename, index=False)

    def end(self):
        title = self.get_title()
        self.update_graph(title=title)
        self.dfhistory = pd.DataFrame(self.history)
        return self.dfhistory

    def head(self):
        best_epoch, best_score = self.get_best_score()
        print(f"Best {self.metric_name}: {best_score:.4f} at epoch {best_epoch}")
        return self.dfhistory.head()

    def get_best_score(self):
        dfhistory = pd.DataFrame(self.history)
        arr_scores = dfhistory[self.metric_name]
        best_score = np.max(arr_scores) if self.metric_mode == "max" else np.min(arr_scores)
        best_epoch = dfhistory.loc[arr_scores == best_score, 'epoch'].tolist()[0]
        return (best_epoch, best_score)

    def get_title(self):
        best_epoch, best_score = self.get_best_score()
        title = f'best {self.metric_name}={best_score:.4f} (@epoch {best_epoch})'
        return title

    def update_graph(self, title=None, x_bounds=None, y_bounds=None):
        if not hasattr(self, 'graph_fig'):
            self.fig, self.ax = plt.subplots(1, figsize=self.figsize)
        self.ax.clear()

        dfhistory = pd.DataFrame(self.history)
        epochs = dfhistory['epoch'] if 'epoch' in dfhistory.columns else []

        metric_name = self.metric_name.replace('val_', '').replace('train_', '')

        m1 = "train_" + metric_name
        if m1 in dfhistory.columns:
            train_metrics = dfhistory[m1]
            self.ax.plot(epochs, train_metrics, 'bo--', label=m1, clip_on=False)

        m2 = 'val_' + metric_name
        if m2 in dfhistory.columns:
            val_metrics = dfhistory[m2]
            self.ax.plot(epochs, val_metrics, 'co-', label=m2, clip_on=False)

        if metric_name in dfhistory.columns:
            metric_values = dfhistory[metric_name]
            self.ax.plot(epochs, metric_values, 'co-', label=self.metric_name, clip_on=False)

        self.ax.set_xlabel("epoch")
        self.ax.set_ylabel(metric_name)

        if title:
            self.ax.set_title(title)

        if m1 in dfhistory.columns or m2 in dfhistory.columns or self.metric_name in dfhistory.columns:
            self.ax.legend(loc='best')

        if len(epochs) > 0:
            best_epoch, best_score = self.get_best_score()
            self.ax.plot(best_epoch, best_score, 'r*', markersize=15, clip_on=False)

        if x_bounds is not None: self.ax.set_xlim(*x_bounds)
        if y_bounds is not None: self.ax.set_ylim(*y_bounds)
        self.fig.savefig(self.save_path)
        plt.close()




if __name__=='__main__':
    # import random
    # epochs = 20
    # vlog = ProcessMonitor(epochs=epochs, metric='train_loss', mode='min')
    # vlog.start()
    # for epoch in range(1, epochs + 1):
    #     train_loss = random.uniform(0.5, 2.0)
    #     val_loss = random.uniform(0.4, 1.5)
    #     vlog.log_epoch({'train_loss': train_loss, 'val_loss': val_loss})
    #
    # vlog.end()
    # print(vlog.head())
    #
    #
    # vlog = ProcessMonitor(epochs=epochs, metric='psnr', mode='max')
    # for epoch in range(1, epochs + 1):
    #     psnr = random.uniform(25, 42)
    #     vlog.log_epoch({'psnr': psnr})
    #
    # vlog.end()
    # print(vlog.head())

    true = torch.tensor([0, 1, 2, 0, 3, 2, 4])
    pred = torch.tensor([0, 1, 1, 0, 3, 1, 4])  # 第三个样本预测错误
    cm = ConfusionMatrixRecord(num_classes=5)
    cm.update(true, pred)
    print(cm)






