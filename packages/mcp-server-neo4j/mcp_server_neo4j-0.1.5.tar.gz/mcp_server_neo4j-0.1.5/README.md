# Neo4j MCP 服务器

一个基于 Model Context Protocol 的 Neo4j 图数据库操作服务器。该服务器使 LLM 能够执行 Neo4j 数据库操作，包括运行 Cypher 查询和获取数据库元信息。

## 可用工具

- `run_query` - 执行 Cypher 查询语句
  - 必需参数:
    - `query` (字符串): Cypher 查询语句
  - 可选参数:
    - `parameters` (对象): 查询参数

- `get_database_info` - 获取 Neo4j 数据库信息
  - 无需参数

- `get_node_labels` - 获取数据库中所有节点标签
  - 无需参数

- `get_relationship_types` - 获取数据库中所有关系类型
  - 无需参数

- `get_node_properties` - 获取指定标签节点的属性信息
  - 必需参数:
    - `label` (字符串): 节点标签名称

## 安装

### 使用 uv (推荐)

当使用 [`uv`](https://docs.astral.sh/uv/) 时，不需要特定安装。我们将使用 [`uvx`](https://docs.astral.sh/uv/guides/tools/) 直接运行 *mcp-server-neo4j*。

### 使用 PIP

您也可以通过 pip 安装 `mcp-server-neo4j`:

```bash
pip install mcp-server-neo4j
```

安装后，您可以通过以下命令运行:

```bash
python -m mcp_server_neo4j
```

### Docker 构建

```bash
cd src/neo4j
docker build -t mcp/neo4j .
```

## 配置

### 配置 Claude.app

在 Claude 设置中添加:

<details>
<summary>使用 uvx</summary>

```json
"mcpServers": {
  "neo4j": {
    "command": "uvx",
    "args": ["mcp-server-neo4j", "--uri=bolt://neo4j-server:7687", "--username=neo4j", "--password=your_password"]
  }
}
```
</details>

<details>
<summary>使用 docker</summary>

```json
"mcpServers": {
  "neo4j": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "mcp/neo4j", "--uri=bolt://neo4j-server:7687", "--username=neo4j", "--password=your_password"]
  }
}
```
</details>

<details>
<summary>使用 pip 安装</summary>

```json
"mcpServers": {
  "neo4j": {
    "command": "python",
    "args": ["-m", "mcp_server_neo4j", "--uri=bolt://neo4j-server:7687", "--username=neo4j", "--password=your_password"]
  }
}
```
</details>

### 配置 Zed

在 Zed 的 settings.json 中添加:

<details>
<summary>使用 uvx</summary>

```json
"context_servers": [
  "mcp-server-neo4j": {
    "command": "uvx",
    "args": ["mcp-server-neo4j", "--uri=bolt://neo4j-server:7687", "--username=neo4j", "--password=your_password"]
  }
],
```
</details>

<details>
<summary>使用 pip 安装</summary>

```json
"context_servers": {
  "mcp-server-neo4j": {
    "command": "python",
    "args": ["-m", "mcp_server_neo4j", "--uri=bolt://neo4j-server:7687", "--username=neo4j", "--password=your_password"]
  }
},
```
</details>

## 调试

您可以使用 MCP inspector 来调试服务器。对于 uvx 安装:

```bash
npx @modelcontextprotocol/inspector uvx mcp-server-neo4j
```

或者，如果您在特定目录中安装了该包或正在开发:

```bash
cd path/to/servers/src/neo4j
npx @modelcontextprotocol/inspector uv run mcp-server-neo4j
```

## 示例交互

1. 执行 Cypher 查询:
```json
{
  "name": "run_query",
  "arguments": {
    "query": "MATCH (n:Person) RETURN n.name, n.age LIMIT 10"
  }
}
```
响应:
```json
{
  "data": [
    {
      "n.name": "张三",
      "n.age": 30
    },
    {
      "n.name": "李四",
      "n.age": 25
    }
  ],
  "summary": {
    "counters": {
      "nodes_created": 0,
      "nodes_deleted": 0,
      "relationships_created": 0,
      "relationships_deleted": 0,
      "properties_set": 0,
      "labels_added": 0,
      "labels_removed": 0,
      "indexes_added": 0,
      "indexes_removed": 0,
      "constraints_added": 0,
      "constraints_removed": 0
    }
  }
}
```

2. 获取数据库信息:
```json
{
  "name": "get_database_info",
  "arguments": {}
}
```
响应:
```json
{
  "name": "Neo4j",
  "version": "5.14.0",
  "node_count": 1000,
  "relationship_count": 5000,
  "labels": ["Person", "Movie", "Director"],
  "relationship_types": ["ACTED_IN", "DIRECTED", "FRIEND_OF"]
}
```

## Claude 使用示例问题

1. "你能帮我查询图数据库中的所有人物节点吗？"
2. "请告诉我数据库中有哪些类型的节点标签和关系"
3. "执行查询，找出所有演员和他们参演的电影"
4. "Person 节点有哪些属性？"

## 贡献

我们鼓励您对 mcp-server-neo4j 进行贡献。无论您想添加新的 Neo4j 相关工具、增强现有功能，还是改进文档，您的贡献都是宝贵的。

有关其他 MCP 服务器和实现模式的示例，请参阅:
https://github.com/modelcontextprotocol/servers

欢迎提交拉取请求！欢迎贡献新想法、错误修复或增强功能，以使 mcp-server-neo4j 更加强大和有用。

## 许可证

mcp-server-neo4j 遵循 MIT 许可证。这意味着您可以自由使用、修改和分发该软件，但须遵守 MIT 许可证的条款和条件。有关更多详细信息，请参阅项目代码库中的 LICENSE 文件。 