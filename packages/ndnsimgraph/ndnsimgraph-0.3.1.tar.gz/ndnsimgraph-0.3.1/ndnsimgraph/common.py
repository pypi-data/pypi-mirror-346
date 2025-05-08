import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections.abc import Callable
from typing import List
from matplotlib.axes import Axes


def getRandomColor():
    """获取一个随机的颜色"""
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


class NodeItem:
    def __init__(self, nodeName, nodeId, label: str = None):
        self.nodeName = nodeName
        self.nodeId = nodeId
        self.label = nodeName if label is None else label


class GraphBase:
    """
    一个基于 matplotlib 实现的通用绘图接口
    """

    def __init__(self):
        # 记录所有可用的 Marker
        # https://matplotlib.org/stable/api/markers_api.html
        self.markers = ["o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+",
                        "x", "X", "D", "d", "|", "_", ".", ","]
        # 记录当前图已经使用的Marker
        self.currentUsedMarker = {}
        # 记录常用的 color
        self.colors = [
            "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",
            "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan", "red", "green", "blue", "c", "m", "y",
        ]
        # 记录当前图已经使用的 color
        self.currentUsedColor = {}
        # 记录常用的 hatch
        self.hatches = ['', '/', 'o', 'x', '.', '\\', 'O', '|', '-', '+', 'x', '*',
                        '/o', '\\|', '|*', '-\\', '+o', 'x*', 'o-', 'O|', 'O.', '*-']
        self.currentUsedHatch = {}
        # 字体大小
        self.fontSize = 12
        # plotFilter
        self.plotFilter: Callable[[float, float, str, str, str], bool] = None
        # platMap
        self.plotMap: Callable[[List[float], List[float], str, str, str], (List[float], List[float])] = None
        # bindAx
        self.ax: Axes = None

    def bindAxes(self, ax: Axes):
        """
        绑定一个 ax 对象，用于绘图
        :param ax:
        :return:
        """
        self.ax = ax
        return self

    def setPlotFilter(self, plotFilter: Callable[[float, float, str, str, str], bool]):
        """
        设置 plot 函数过滤器，
        [x_value, y_value, nodeName, nodeId, label] => bool value indicate is selected
        :return:
        """
        self.plotFilter = plotFilter
        return self

    def setPlotMap(self, plotMap: Callable[[List[float], List[float], str, str, str], (List[float], List[float])]):
        """
        设置 plot 转换器
        [x, y, nodeName, nodeId, label] => [new_x, new_y]
        :param plotMap:
        :return:
        """
        self.plotMap = plotMap
        return self

    def setFontSize(self, fontSize: int):
        """
        设置字体大小
        :param fontSize:
        :return:
        """
        self.fontSize = fontSize
        return self

    def autoSelectHatch(self) -> str:
        """
        从所有的候选 Hatch 中自动选择
        :return:
        """
        for hatch in self.hatches:
            if hatch not in self.currentUsedHatch:
                self.currentUsedHatch[hatch] = hatch
                return hatch
        return ""

    def autoSelectMarker(self) -> str:
        """
        从所有的marker中自动选择 Marker，保证不和已有的Marker重复
        :return:
        """
        for marker in self.markers:
            if marker not in self.currentUsedMarker:
                self.currentUsedMarker[marker] = marker
                return marker
        return ""

    def autoSelectColor(self) -> str:
        for color in self.colors:
            if color not in self.currentUsedColor:
                return color
        while True:
            randomColor = getRandomColor()
            if randomColor not in self.currentUsedColor:
                break
            self.currentUsedColor[randomColor] = randomColor
        return randomColor

    def tick_direction(self, direction: str):
        """
        设置坐标轴 ticker 的方向，可以取 ['in', 'out', 'inout']
        :param direction:
        :return:
        """
        if self.ax is not None:
            pass
            self.ax.tick_params(direction=direction)
        else:
            plt.rcParams['xtick.direction'] = direction
            plt.rcParams['ytick.direction'] = direction
        return self

    def grid(self, *args, **kwargs):
        if self.ax is not None:
            self.ax.grid(*args, **kwargs)
        else:
            plt.grid(*args, **kwargs)
        return self

    def xlim(self, *args, **kwargs):
        if self.ax is not None:
            self.ax.set_xlim(*args, **kwargs)
        else:
            plt.xlim(*args, **kwargs)
        return self

    def ylim(self, *args, **kwargs):
        if self.ax is not None:
            self.ax.set_ylim(*args, **kwargs)
        else:
            plt.ylim(*args, **kwargs)
        return self

    def ticker_params(self, axis='both', **kwargs):
        if self.ax is not None:
            self.ax.tick_params(axis, **kwargs)
        else:
            plt.tick_params(axis, **kwargs)
        return self

    def xticks(self, ticks=None, labels=None, **kwargs):
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = self.fontSize
        if self.ax is not None:
            self.ax.tick_params(labelsize=self.fontSize)
            if ticks is not None:
                self.ax.set_xticks(ticks, labels, **kwargs)
        else:
            plt.xticks(ticks, labels, **kwargs)
        return self

    def yticks(self, ticks=None, labels=None, **kwargs):
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = self.fontSize
        if self.ax is not None:
            self.ax.tick_params(labelsize=self.fontSize)
            if ticks is not None:
                self.ax.set_yticks(ticks, labels, **kwargs)
        else:
            plt.yticks(ticks, labels, **kwargs)
        return self

    def title(self, label, fontdict=None, loc=None, pad=None, **kwargs):
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = self.fontSize
        if self.ax is not None:
            self.ax.set_title(label, fontdict=fontdict, loc=loc, pad=pad, **kwargs)
        else:
            plt.title(label, fontdict=fontdict, loc=loc, pad=pad, **kwargs)
        return self

    def xlabel(self, xlabel, fontdict=None, labelpad=None, loc=None, **kwargs):
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = self.fontSize
        if self.ax is not None:
            self.ax.set_xlabel(xlabel, fontdict, labelpad, loc=loc, **kwargs)
        else:
            plt.xlabel(xlabel, fontdict, labelpad, loc=loc, **kwargs)
        return self

    def ylabel(self, ylabel, fontdict=None, labelpad=None, loc=None, **kwargs):
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = self.fontSize
        if self.ax is not None:
            self.ax.set_ylabel(ylabel, fontdict, labelpad, loc=loc, **kwargs)
        else:
            plt.ylabel(ylabel, fontdict, labelpad, loc=loc, **kwargs)
        return self

    def legend(self, markerSize: int = None, markerEdgeWidth: int = None,
               *args, **kwargs):
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = self.fontSize
        if self.ax is not None:
            lgnd = self.ax.legend(*args, **kwargs)
        else:
            lgnd = plt.legend(*args, **kwargs)
        if markerSize is not None:
            for leg in lgnd.get_lines():
                leg.set_markersize(markerSize)
        if markerEdgeWidth is not None:
            for leg in lgnd.get_lines():
                leg.set_markeredgewidth(markerEdgeWidth)
        return self

    def _do_filter(self, filter_func, x: List[float], y: List[float], *args):
        cp_x, cp_y = x.copy(), y.copy()
        x, y = [], []
        for i in range(len(cp_x)):
            if filter_func(cp_x[i], cp_y[i], *args):
                x.append(cp_x[i])
                y.append(cp_y[i])
        return x, y

    def _do_map(self, map_func, x: List[float], y: List[float], *args):
        return map_func(x, y, *args)

    def innerPlot(self, x, y, *args,
                  color: str = "&&",
                  linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
                  markerfacecolor: str = "none", markersize: float = 6,
                  **kwargs):
        if "linewidth" not in kwargs:
            kwargs["linewidth"] = linewidth
        if "linestyle" not in kwargs:
            kwargs["linestyle"] = linestyle
        # 默认自动选择Marker
        if marker == "&&":
            marker = self.autoSelectMarker()
            self.currentUsedMarker[marker] = marker
        if "marker" not in kwargs:
            kwargs["marker"] = marker
        if "markerfacecolor" not in kwargs:
            kwargs["markerfacecolor"] = 'none'
        if "markersize" not in kwargs:
            kwargs["markersize"] = markersize
        # 默认自动选择 color
        if color == "&&":
            color = self.autoSelectColor()
            self.currentUsedColor[color] = color
        if "color" not in kwargs:
            kwargs["color"] = color

        nodeName, nodeId, label = kwargs.pop("nodeName", ""), kwargs.pop("nodeId", ""), kwargs.get("label", "")
        if self.plotFilter is not None:
            x, y = self._do_filter(self.plotFilter, x, y, nodeName, nodeId, label)

        if self.plotMap is not None:
            x, y = self._do_map(self.plotMap, x, y, nodeName, nodeId, label)

        if self.ax is not None:
            self.ax.plot(x, y, *args, **kwargs)
        else:
            plt.plot(x, y, *args, **kwargs)
        return self

    def innerPlotSum(self, nodeList: [NodeItem], getNode, getX, getY, *args,
                     color: str = "&&",
                     linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
                     markerfacecolor: str = "none", markersize: float = 6,
                     **kwargs):
        xMerge = []
        yArr = []
        for nodeItem in nodeList:
            node = getNode(nodeItem.nodeName)
            if not node:
                print("not exist node: ", node)
                continue

            x, y = getX(node, nodeItem.nodeId), \
                   getY(node, nodeItem.nodeId)

            if len(x) > len(xMerge):
                xMerge = x
            yArr.append(np.array(y))

        if len(yArr) <= 0:
            return self

        yMerge = np.zeros(len(xMerge))
        # pad y
        for y in yArr:
            y = np.pad(y, (0, len(xMerge) - len(y)), 'constant', constant_values=(0, 0))
            yMerge += y

        if "label" not in kwargs:
            kwargs["label"] = "Merge"

        self.innerPlot(xMerge, yMerge, *args,
                       color=color,
                       linewidth=linewidth,
                       linestyle=linestyle,
                       marker=marker,
                       markerfacecolor=markerfacecolor,
                       markersize=markersize,
                       **kwargs)
        return self

    def innerPlotAvg(self, nodeList: [NodeItem], getNode, getX, getY, *args,
                     color: str = "&&",
                     linewidth: float = 2, linestyle: str = "dotted", marker: str = "&&",
                     markerfacecolor: str = "none", markersize: float = 6,
                     **kwargs):
        xMerge = []
        yArr = []

        for nodeItem in nodeList:
            node = getNode(nodeItem.nodeName)
            x, y = getX(node, nodeItem.nodeId), \
                   getY(node, nodeItem.nodeId)
            if not node:
                print("not exist node: ", node)
                continue
            if len(x) > len(xMerge):
                xMerge = x
            yArr.append(np.array(y))

        if len(yArr) <= 0:
            return self

        yMerge = np.zeros(len(xMerge))

        # pad y
        for y in yArr:
            y = np.pad(y, (0, len(xMerge) - len(y)), 'constant', constant_values=(0, 0))
            yMerge += y
        yMerge /= len(yArr)

        if "label" not in kwargs:
            kwargs["label"] = "Merge"

        if self.plotFilter is not None:
            x, y = self._do_filter(self.plotFilter, x, y, nodeName, nodeId)

        if self.plotMap is not None:
            x, y = self._do_map(self.plotMap, x, y, nodeName, nodeId)

        self.innerPlot(xMerge, yMerge, *args,
                       color=color,
                       linewidth=linewidth,
                       linestyle=linestyle,
                       marker=marker,
                       markerfacecolor=markerfacecolor,
                       markersize=markersize,
                       **kwargs)
        return self

    def show(self, *args, **kwargs):
        """
        绘制吞吐量图，并show
        :return:
        """
        plt.show(*args, **kwargs)
        return self

    def drawAndSave(self, dir: str, name: str, *args, **kwargs):
        """
        绘制吞吐量图，并保存到图片当中
        :return:
        """
        if not os.path.exists(dir):
            os.makedirs(dir)
        # plt.tight_layout()
        plt.savefig(f"{dir}{os.sep}{name}", *args, **kwargs)
        return self

    def close(self):
        plt.close()
        return self


class ExportItem:
    def __init__(self, nodeName: str,
                 units: str, label: str, x: [float], y: [float]):
        self.nodeName = nodeName
        self.units = units
        self.label = label
        self.x = x
        self.y = y


class ExportBase:
    """
    导出基类，用于将统计数据导出到Excel当中
    """

    def __init__(self, getNode=None, getX=None, getY=None, getUnit=None):
        self.items: [ExportItem] = []
        self.getNode = getNode
        self.getX = getX
        self.getY = getY
        self.getUnit = getUnit

    def select(self, nodeName: str, faceId: any, label: str = None):
        if self.getNode is None or self.getX is None or self.getUnit is None:
            print("getNode is None, can not invoke select")
            return self
        node = self.getNode(nodeName)
        if not node:
            print("not exist node: ", node)
            return self
        if label is None:
            label = nodeName
        x, y = self.getX(node, faceId), self.getY(node, faceId)
        self.items.append(
            ExportItem(
                nodeName,
                self.getUnit(),
                label,
                x,
                y))
        return self

    def selectAvg(self, nodeList: [NodeItem], label: str = None):
        if self.getNode is None or self.getX is None or self.getUnit is None:
            print("getNode is None, can not invoke selectAvg")
            return self
        xMerge = []
        yArr = []

        for nodeItem in nodeList:
            node = self.getNode(nodeItem.nodeName)
            x, y = self.getX(node, nodeItem.nodeId), self.getY(node, nodeItem.nodeId)
            if not node:
                print("not exist node: ", node)
                continue
            if len(x) > len(xMerge):
                xMerge = x
            yArr.append(np.array(y))

        if len(yArr) <= 0:
            return self

        yMerge = np.zeros(len(xMerge))

        # pad y
        for y in yArr:
            y = np.pad(y, (0, len(xMerge) - len(y)), 'constant', constant_values=(0, 0))
            yMerge += y
        yMerge /= len(yArr)
        self.items.append(
            ExportItem(
                label,
                self.getUnit(),
                label,
                xMerge,
                yMerge))
        return self

    def selectSum(self, nodeList: [NodeItem], label: str = None):
        if self.getNode is None or self.getX is None or self.getUnit is None:
            print("getNode is None, can not invoke selectSum")
            return self
        xMerge = []
        yArr = []

        for nodeItem in nodeList:
            node = self.getNode(nodeItem.nodeName)
            x, y = self.getX(node, nodeItem.nodeId), self.getY(node, nodeItem.nodeId)
            if not node:
                print("not exist node: ", node)
                continue
            if len(x) > len(xMerge):
                xMerge = x
            yArr.append(np.array(y))

        if len(yArr) <= 0:
            return self

        yMerge = np.zeros(len(xMerge))

        # pad y
        for y in yArr:
            y = np.pad(y, (0, len(xMerge) - len(y)), 'constant', constant_values=(0, 0))
            yMerge += y
        self.items.append(
            ExportItem(
                label,
                self.getUnit(),
                label,
                xMerge,
                yMerge))
        return self

    def _get_statistical_info_dataframe(self):
        statistics_columns = [
            'Node', 'Label', 'Units', 'Sample Counts',
            'Sum', 'Avg', 'Mean', 'Var', 'std'
        ]
        statistics_data = []
        for item in self.items:
            statistics_data.append([
                item.nodeName,
                item.label,
                item.units,
                len(item.y),
                round(np.sum(item.y), 3),
                round(np.average(item.y), 3),
                round(np.mean(item.y), 3),
                round(np.var(item.y), 3),
                round(np.std(item.y), 3)
            ])

        return pd.DataFrame(statistics_data, columns=statistics_columns)

    def save_statistical_info_as_csv(
            self, save_dir: str, filename: str
    ):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self._get_statistical_info_dataframe(). \
            to_csv(f"{save_dir}{os.sep}{filename}")
        return self

    def save_statistical_info_as_excel(
            self, save_dir: str, filename: str
    ):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self._get_statistical_info_dataframe(). \
            to_excel(f"{save_dir}{os.sep}{filename}")
        return self

    def print_statistical_info_as_latex(self):
        print(self._get_statistical_info_dataframe().style.to_latex())
        return self

    def print_statistical_info_as_table(self, title: str):
        """
        以表格的形式打印统计信息
        :return:
        """
        from rich.console import Console
        from rich.table import Table
        console = Console()

        table = Table(show_header=True,
                      header_style="bold magenta",
                      title=title, expand=True)
        table.add_column("Node", justify="center", no_wrap=True)
        table.add_column("Label", justify="center", no_wrap=True)
        table.add_column("Units", justify="center", no_wrap=True)
        table.add_column("Sample Counts", justify="center", no_wrap=True)
        table.add_column("Sum", justify="center", no_wrap=True)
        table.add_column("Average", justify="center", no_wrap=True)
        table.add_column("Mean", justify="center", no_wrap=True)
        table.add_column("Var", justify="center", no_wrap=True)
        table.add_column("Std", justify="center", no_wrap=True)
        for item in self.items:
            table.add_row(
                item.nodeName,
                item.label,
                item.units,
                str(len(item.y)),
                str(round(np.sum(item.y), 3)),
                str(round(np.average(item.y), 3)),
                str(round(np.mean(item.y), 3)),
                str(round(np.var(item.y), 3)),
                str(round(np.std(item.y), 3))
            )
        console.print(table)
        return self

    def exportCDFExcel(self,
                       save_dir: str,
                       filename: str,
                       savePath: str,
                       xName: str = "Rate",
                       yName: str = "CDF"):
        """
        计算CDF（Cumulative Distribution Function）并导出
        :param xName:
        :param yName:
        :param savePath:
        :return:
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = f"{save_dir}{os.sep}{filename}"
        longNames, units, labels = [], [], []
        ys, maxLen = [], 0

        for item in self.items:
            maxLen = max(maxLen, len(item.y))

        for item in self.items:
            y = np.array(np.pad(item.y, (0, maxLen - len(item.y)), 'constant', constant_values=(0, 0))).T
            x = np.sort(y)
            ys.append(x)
            longNames.append(xName)
            units.append(item.units)
            labels.append(item.label)
            y = 1. * np.arange(len(x)) / (len(x) - 1)
            ys.append(y)
            longNames.append(yName)
            units.append("")
            labels.append(item.label)

        contents = []
        # long name
        contents.append(longNames)

        # units
        contents.append(units)

        # comments
        contents.append(labels)

        dataMatrix = np.vstack(ys)

        # write datas
        for i in range(maxLen):
            contents.append(dataMatrix[:, i])

        df = pd.DataFrame(contents)
        df.to_excel(save_path, index=False, header=None)
        return self

    def exportExcel(self,
                    save_dir: str,
                    filename: str,
                    xName: str = "Times",
                    yName: str = "Rate",
                    xUnit: str = "Second"):
        """
        导出数据到Excel
        :param savePath:
        :param xName:
        :param yName:
        :param xUnit:
        :return:
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = f"{save_dir}{os.sep}{filename}"
        contents = []
        nodeNames, units, labels, xResult = [], [], [], []
        for item in self.items:
            nodeNames.append(item.nodeName)
            units.append(item.units)
            labels.append(item.label)
            if len(item.x) > len(xResult):
                xResult = item.x
        # long name
        contents.append([xName] + [yName for _ in range(len(nodeNames))])

        # units
        contents.append([xUnit] + units)

        # comments
        contents.append([""] + labels)

        ys = [xResult]
        # padding y
        for item in self.items:
            ys.append(np.array(np.pad(item.y, (0, len(xResult) - len(item.y)), 'constant', constant_values=(0, 0))).T)

        dataMatrix = np.vstack(ys)

        # write datas
        for i in range(len(xResult)):
            contents.append(dataMatrix[:, i])

        df = pd.DataFrame(contents)
        df.to_excel(save_path, index=False, header=None)
        return self
