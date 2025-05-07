# ONNX Checker

[![PyPI version]][pypi-url] [![License]][license-url]

`onnx-check` is a lightweight CLI that **inspects ONNX models *before* you convert or deploy them**. It tells you exactly which operators the graph uses and whether they are supported on your target hardware.

> "Catch unsupported operators early – before they derail your model."
> — *Mason Huang*

## ✨ Features (v0.1)

| Feature               | Description                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Operator scan**     | Fast, dependency‑free static analysis of `.onnx` files                                                                                |
| **Hardware profiles** | Built‑in JSON compatibility tables for common NPUs (Currently only KL520, 530, 630, 720, 730 …) with an easy override mechanism |
| **Clear report**      | CLI table plus optional JSON / Markdown export; highlights unsupported ops and optional‑feature gaps                                  |
| **Actionable hints**  | Suggestions and links to official docs for each unsupported operator                                                                  |

<details>
<summary>Roadmap</summary>

| Milestone | Planned                                  | Notes                                                    |
| --------- | ---------------------------------------- | -------------------------------------------------------- |
| **0.2**   | Markdown/JSON report templates           | Nice for CI bots                                         |
| **0.3**   | Model slimming (`--prune`, `--quantize`) | Reduce model size before flashing                        |
| **0.4**   | Automatic op replacement (`--replace`)   | Swap unsupported ops for functionally‑equivalent kernels |
| **0.5**   | Interactive web viewer (`onnx-op-view`)  | Drag‑and‑drop visualiser                                 |

</details>


## 🚀 Quick start
| Command                                           | Description                                           |
|---------------------------------------------------|-------------------------------------------------------|
| `pip install onnx-checker`                        | Install latest package from PyPI                                     |
| `onnxcheck my_model.onnx -p KL720`                | Inspect `my_model.onnx` for the KL720 hardware profile |
| `onnxcheck my_model.onnx`                         | Inspect `my_model.onnx` for all built-in profiles      |
| `onnxcheck -V`, `onnxcheck --version` | Show onnx-checker version                    |



### Sample output

```
Model summary – my_model.onnx
IR version : 6    Opset : 11
Inputs  : input  float32  [1, 3, 112, 112]
Outputs : output  float32  [1, 512]
Dynamic axes : None detected ✓

my_model.onnx · IR 6 · KL520
╭──────────────────────────────────────────────────────────────╮
│  Status  Operator   Count   Notes                            │
├──────────────────────────────────────────────────────────────┤
│   ✓      Conv        27                                      │
│   ✓      Relu        27                                      │
│   ✗      Elu          5     Not supported on KL520           │
│   ✓      MaxPool      5                                      │
│   ✗      Resize       2     Only linear/nearest modes OK     │
╰──────────────────────────────────────────────────────────────╯
⚠  2 unsupported operator(s) detected.
```

<!-- ## 🛠️ Development & Publishing

透過 Poetry 一鍵建置與發佈：

```bash
# 1. build wheel and sdist
poetry build

# 2. （Test version）publish to TestPyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi <YOUR_TEST_PYPI_TOKEN>
poetry publish -r testpypi

# 3. Publish official version to PyPI
poetry config pypi-token.pypi <YOUR_PYPI_TOKEN>
poetry publish
``` -->

## 🧑‍💻 API usage

```python
from onnx_op_check import Checker, load_profile

checker = Checker("my_model.onnx", profile=load_profile("kl720"))
report = checker.run()
print(report.to_markdown())
```


## 📖 Hardware profiles

Profiles live under `onnx_op_check/profiles/*.json`.
Each profile declares the operators, attributes, and constraints supported by a particular accelerator.
See [`docs/PROFILE_SCHEMA.md`](docs/PROFILE_SCHEMA.md) for the JSON schema.

Contributions for new hardware are very welcome!

## 🤝 Contributing

We love pull requests! Please read `CONTRIBUTING.md` and open an issue before you start a large refactor so we can align on design.

Coding conventions follow **PEP 8** with the Black formatter.

## 📜 License

Released under the **MIT License** © 2025 Mason & contributors.

### A note on language

The primary language of this README is **English** for wider community reach.  A Traditional Chinese translation will be added soon in `docs/README_zh-TW.md`.


[PyPI version]: https://img.shields.io/pypi/v/onnx-checker
[pypi-url]: https://pypi.org/project/onnx-checker
[Build status]: https://img.shields.io/github/actions/workflow/status/HuangMason320/onnx-checker/ci.yml?branch=main
[ci-url]: https://github.com/HuangMason320/onnx-checker/actions
[License]: https://img.shields.io/github/license/HuangMason320/onnx-checker
[license-url]: https://pypi.org/project/onnx-checker/
