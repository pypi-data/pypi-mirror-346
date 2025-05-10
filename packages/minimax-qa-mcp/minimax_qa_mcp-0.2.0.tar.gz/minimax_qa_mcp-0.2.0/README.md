# QA - agent service 集合

## 项目结构
- `server.py`: MCP接口定义和服务启动入口
- `src/`: 核心功能模块实现
- `conf/`: 配置文件
- `utils/`: 工具函数
- `logs/`: 日志文件夹

## 功能特性
1. 天气服务(demo)：
   - 获取美国各州天气警报信息
   - 基于经纬度获取天气预报

2. 日志检索服务：
   - 从Grafana获取各业务服务的日志
   - 支持按关键字、时间等条件筛选
   - 支持获取服务接口列表

## 环境配置与启动

项目现在使用ux进行构建和打包，提供了多种安装运行方式。

### 1. 从PyPI安装

```shell
# 直接从PyPI安装
pip install minimax-qa-mcp

# 运行服务
minimax-qa-mcp
```

### 2. 开发模式

```shell
# 安装依赖
pip install ux
pip install -r requirements.txt

# 开发模式运行
bash run.sh
# 或
ux run
```

### 3. 构建与发布

```shell
# 构建项目
bash build.sh

# 发布到PyPI
bash publish.sh
```

### 4. 查看启动
```
本地生成 log/agent_log.log文件，且打印 
INFO:     Uvicorn running on http://0.0.0.0:8888 (Press CTRL+C to quit)
```

### 5. 集成到MCP客户端

#### curl
 ```shell
http://0.0.0.0:8888/sse
 ```

#### Python模块方式
```shell
python -m minimax_qa_mcp.server
```

#### Claude Desktop 配置
```json
{
    "agent_name": {
      "command": "minimax-qa-mcp",
      "args": ["--host", "0.0.0.0", "--port", "8888"]
    }
}
```

## API 说明

### 天气服务(demo)
- `get_alerts(state)`: 获取指定州的天气警报
- `get_forecast(latitude, longitude)`: 获取指定位置的天气预报

### 日志服务
- `get_grafana_data(scene, psm, msg, from_time, to_time)`: 获取业务的grafana日志
- `get_top_methods(scene, psm)`: 获取服务存在调用的接口列表
- `get_http_data(scene, psm, api_path, from_time, to_time)`: 获取业务http接口流量日志
- `query_code_segments(query, query_type, limit, exact, advanced, depth, direction, output)`: 查询代码片段
- `gen_case(input_data, pwd)`: 生成link_case
- `get_weaviate_info(input_data)`: 获取业务相关信息
