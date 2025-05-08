# Power Calculator Zimjing

一个简单而强大的Python包，用于计算数值的乘方。

## 功能特点

- 支持整数和小数的乘方计算
- 支持负数指数
- 支持零次方计算
- 类型提示支持
- 完整的文档字符串

## 安装

使用pip安装：

```bash
pip install power-calculator-zimjing
```

## 使用方法

```python
from power_calculator_zimjing import power

# 计算2的3次方
result = power(2, 3)  # 返回 8.0

# 计算2.5的平方
result = power(2.5, 2)  # 返回 6.25

# 计算5的0次方
result = power(5, 0)  # 返回 1.0

# 计算2的-1次方
result = power(2, -1)  # 返回 0.5
```

## 参数说明

`power(base: float, exponent: float) -> float`

- `base`: 底数，可以是整数或小数
- `exponent`: 指数，可以是整数、小数或负数
- 返回值: 计算结果，类型为 float

## 开发

1. 克隆仓库
```bash
git clone https://github.com/zimjing/power-calculator.git
cd power-calculator
```

2. 安装开发依赖
```bash
pip install -e .
```

3. 运行测试
```bash
pytest tests/
```

## 项目结构

```
power-calculator/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── power_calculator_zimjing/
│       ├── __init__.py
│       └── example.py
└── tests/
    └── test_example.py
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目使用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 作者

- Zim Jing
- 邮箱：340552684@qq.com

## 版本历史

- 0.1.0 (2024-03-21)
  - 首次发布
  - 实现基本的乘方计算功能