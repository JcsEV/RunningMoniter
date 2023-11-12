# RunningMoniter
 基于Tensorflow的跑步运动检测

“跑步检测”是一款应用于安卓平台的手机应用，可以实时监测不良坐姿并给出提示。本项目主要基于 [Tensorflow Lite 官方示例 - 姿态估计](https://github.com/tensorflow/examples/tree/master/lite/examples/pose_estimation/android)实现，其中 AI 部分包含用于姿态估计的 [MoveNet](https://blog.tensorflow.org/2021/05/next-generation-pose-detection-with-movenet-and-tensorflowjs.html)，以及用于对姿态进行分类的[全连接网络](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/tutorials/pose_classification.ipynb)。本应用不需要联网使用，所有 AI 特性均在手机本地运行，不需要将视频画面传输至外部服务器，仅需要摄像头权限用于获取姿态画面。

### 文件结构

```bash
├───running-moniter
│   ├───app
│   │   └───src
│   └───gradle
├───movenet
│   └───data
│       └───run_predict
│       └───running_pic
│       └───running_vid
```

项目的两个主要文件夹为 `running-moniter/` 与 `movenet/`。`running-moniter/` 下包含了所有与移动 App 相关的代码，`movenet/` 文件夹下则是分类网络的训练数据与记录了训练过程的 `movenet.ipynb` 文件，训练数据存放在 `movenet/data/run_predict/` 目录下，为精简项目体积，未上传对应数据集。如果需要训练分类模型，可以按 `movenet/pulgin/dataProcess.py` 上面的指示填充 `main/data/run_predict/文件夹。`

## 模型介绍

本项目需要用到两个神经网络模型文件，均已包含在本项目中，不需要额外下载。第一个是 `int8` 格式的 MoveNet Thunder 神经网络模型，可以点击[官方模型文件链接](https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/int8/4)进一步了解。[MoveNet](https://blog.tensorflow.org/2021/05/next-generation-pose-detection-with-movenet-and-tensorflowjs.html) 是谷歌推出的轻量级人体姿态估计模型，有 Thunder 和 Lightning 两个版本。其中 Thunder 版本运行速度较慢，但准确率更高，本项目使用的是 Thunder 版本。该版本又分为 `float16`、`int8` 两种数据格式。其中 `float16` 模型只能在通用 GPU 上运行，而 `int8` 模型既可以运行于通用 GPU 之上，也可以在高通骁龙处理器的 [Hexagon DSP 数字信号处理器](https://developer.qualcomm.com/software/hexagon-dsp-sdk/dsp-processor)上运行。运行在 Hexagon 处理器上时，AI 程序运行速度更快、也更省电，建议对 AI 模型进行移动部署时优先选择 Hexagon 处理器。目前谷歌也推出了自研的 Google Tensor 处理器，最新型号为 Tensor G2，如何调用 Tensor 处理器的 AI 加速单元尚不清楚，未来拿到设备实测确认后会更新文档。

## 鸣谢

本项目主要基于 [Tensorflow Lite Pose Estimation 示例项目](https://github.com/tensorflow/examples/tree/master/lite/examples/pose_estimation/android)，离不开 [Tensorflow](https://www.tensorflow.org/?hl=zh-cn)、[Jupyter Notebook](https://jupyter.org/) 等开源框架、开源开发工具。感谢各位程序工作者对开源社区的贡献！

- [2023.06.20] 感谢 [@linyiLYi](https://github.com/linyiLYi) 对项目实现的启发
