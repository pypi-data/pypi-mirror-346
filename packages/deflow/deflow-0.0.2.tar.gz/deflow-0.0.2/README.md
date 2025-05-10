# DeFlow

A **Lightweight Declarative Data Framework** that build on the
[🏃 Workflow](https://github.com/ddeutils/ddeutil-workflow) package.

I want to use this project is the real-world use-case for my [🏃 Workflow](https://github.com/ddeutils/ddeutil-workflow)
package that able to handle production data pipeline with the DataOps strategy.

> [!WARNING]
> This framework does not allow you to custom your pipeline yet. If you want to
> create you workflow, you can use the [🏃 Workflow](https://github.com/ddeutils/ddeutil-workflow)
> package instead that already installed.

In my opinion, I think it should not create duplicate workflow codes if I can
write with dynamic input parameters on the one template workflow that just change
the input parameters per use-case instead.
This way I can handle a lot of logical workflows in our orgs with only metadata
configuration. It called **Metadata Driven Data Workflow**.

## 📦 Installation

```shell
pip install -U deflow
```

## :dart: Usage

### Version 1

After initialize data framework project with **Version 1**, your data pipeline
config files will store with this file structure:

```text
conf/
 ├─ conn/
 │   ├─ c_conn_01.yml
 │   ╰─ c_conn_02.yml
 ├─ routes/
 │   ╰─ routing.yml
 ╰─ stream/
     ╰─ s_stream_01/
         ├─ g_group_01.tier.priority/
         │   ├─ p_proces_01.yml
         │   ╰─ p_proces_02.yml
         ├─ g_group_02.tier.priority/
         │   ├─ p_proces_01.yml
         │   ╰─ p_proces_02.yml
         ╰─ config.yml
```

You can run the data flow by:

```python
from deflow.flow import Flow
from ddeutil.workflow import Result

flow: Result = Flow(name="s_stream_01").run(mode="N")
```

## :cookie: Configuration

Support data framework version:

|  Version  |  Supported  | Description                                              |
|:---------:|:-----------:|----------------------------------------------------------|
|     1     |     Yes     | A data framework that base on stream, group, and process |

## 💬 Contribute

I do not think this project will go around the world because it has specific propose,
and you can create by your coding without this project dependency for long term
solution. So, on this time, you can open [the GitHub issue on this project 🙌](https://github.com/ddeutils/fastflow/issues)
for fix bug or request new feature if you want it.
