import json
from enum import Enum
from typing import Sequence, Any, List, Dict, Optional
import sys
import logging

from neo4j import GraphDatabase
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError
from neo4j.graph import Path, Node, Relationship

from pydantic import BaseModel, Field

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger('mcp-neo4j')

class Neo4jTools(str, Enum):
    RUN_QUERY = "run_query"
    GET_DATABASE_INFO = "get_database_info"
    GET_NODE_LABELS = "get_node_labels"
    GET_RELATIONSHIP_TYPES = "get_relationship_types"
    GET_NODE_PROPERTIES = "get_node_properties"


class Neo4jResult(BaseModel):
    """Neo4j 查询结果"""
    data: List[Dict[str, Any]] = Field(default_factory=list)
    summary: Optional[Dict[str, Any]] = None


class DatabaseInfo(BaseModel):
    """数据库信息"""
    name: str
    version: str
    node_count: int
    relationship_count: int
    labels: List[str]
    relationship_types: List[str]


class Neo4jServer:
    def __init__(self, uri: str, username: str, password: str, database: str):
        """初始化Neo4j服务器连接"""
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.driver = None

    def _ensure_connection(self):
        """确保数据库连接"""
        if self.driver is None:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
                # 验证连接
                with self.driver.session(database=self.database) as session:
                    session.run("RETURN 1")
                logger.info(f"成功连接到Neo4j数据库: {self.uri}")
            except Exception as e:
                logger.error(f"Neo4j连接失败: {str(e)}")
                raise McpError(f"Neo4j连接失败: {str(e)}")

    def close(self):
        """关闭Neo4j连接"""
        if self.driver is not None:
            logger.info("正在关闭Neo4j连接")
            self.driver.close()
            self.driver = None
            logger.info("Neo4j连接已关闭")

    async def run_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """执行Cypher查询"""
        try:
            self._ensure_connection()
            with self.driver.session(database=self.database) as session:
                result = session.run(query, params or {})
                records = [dict(record) for record in result]
                logger.info(f"查询执行成功，返回 {len(records)} 条记录")
                return records
        except Exception as e:
            logger.error(f"查询执行失败: {str(e)}")
            raise McpError(f"查询执行失败: {str(e)}")

    def get_database_info(self) -> DatabaseInfo:
        """获取数据库信息"""
        try:
            self._ensure_connection()
            with self.driver.session(database=self.database) as session:
                # 获取数据库版本
                version_result = session.run("CALL dbms.components() YIELD name, versions RETURN name, versions")
                version_info = version_result.single()
                name = version_info["name"]
                version = version_info["versions"][0]

                # 获取节点和关系数量
                count_result = session.run("""
                    MATCH (n) 
                    RETURN count(n) as node_count, 
                           size([()-[r]->() | r]) as relationship_count
                """)
                counts = count_result.single()
                node_count = counts["node_count"]
                relationship_count = counts["relationship_count"]

                # 获取所有标签
                labels_result = session.run("CALL db.labels()")
                labels = [record["label"] for record in labels_result]

                # 获取所有关系类型
                rel_types_result = session.run("CALL db.relationshipTypes()")
                relationship_types = [record["relationshipType"] for record in rel_types_result]

                return DatabaseInfo(
                    name=name,
                    version=version,
                    node_count=node_count,
                    relationship_count=relationship_count,
                    labels=labels,
                    relationship_types=relationship_types
                )
        except Exception as e:
            raise McpError(f"获取数据库信息失败: {str(e)}")

    def get_node_labels(self) -> List[str]:
        """获取所有节点标签"""
        try:
            self._ensure_connection()
            with self.driver.session(database=self.database) as session:
                result = session.run("CALL db.labels()")
                return [record["label"] for record in result]
        except Exception as e:
            raise McpError(f"获取节点标签失败: {str(e)}")

    def get_relationship_types(self) -> List[str]:
        """获取所有关系类型"""
        try:
            self._ensure_connection()
            with self.driver.session(database=self.database) as session:
                result = session.run("CALL db.relationshipTypes()")
                return [record["relationshipType"] for record in result]
        except Exception as e:
            raise McpError(f"获取关系类型失败: {str(e)}")

    def get_node_properties(self, label: str) -> Dict[str, List[str]]:
        """获取指定标签节点的属性信息"""
        try:
            self._ensure_connection()
            with self.driver.session(database=self.database) as session:
                # 使用APOC库查询属性（如果可用）
                try:
                    result = session.run(f"""
                        CALL apoc.meta.schema() YIELD value
                        WITH value AS schema
                        RETURN schema.`{label}`.properties AS properties
                    """)
                    if result.peek():
                        properties_data = result.single()["properties"]
                        return {k: [v['type']] for k, v in properties_data.items()}
                except:
                    # 如果APOC不可用，使用备用方法
                    query = f"""
                        MATCH (n:`{label}`)
                        WITH n LIMIT 100
                        UNWIND keys(n) AS key
                        RETURN DISTINCT key, apoc.meta.type(n[key]) AS type
                    """
                    try:
                        result = session.run(query)
                        properties = {record["key"]: [record["type"]] for record in result}
                        return properties
                    except:
                        # 最基本的属性获取方法（无类型信息）
                        query = f"""
                            MATCH (n:`{label}`)
                            WITH n LIMIT 100
                            UNWIND keys(n) AS key
                            RETURN DISTINCT key
                        """
                        result = session.run(query)
                        return {record["key"]: ["未知类型"] for record in result}
        except Exception as e:
            raise McpError(f"获取节点属性失败: {str(e)}")


def serialize_neo4j_obj(obj):
    if isinstance(obj, Path):
        return {
            "nodes": [serialize_neo4j_obj(n) for n in obj.nodes],
            "relationships": [serialize_neo4j_obj(r) for r in obj.relationships]
        }
    elif isinstance(obj, Node):
        return {
            "id": obj.id,
            "labels": list(obj.labels),
            "properties": dict(obj.items())
        }
    elif isinstance(obj, Relationship):
        return {
            "id": obj.id,
            "type": obj.type,
            "start_node": obj.start_node.id,
            "end_node": obj.end_node.id,
            "properties": dict(obj.items())
        }
    elif isinstance(obj, list):
        return [serialize_neo4j_obj(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: serialize_neo4j_obj(v) for k, v in obj.items()}
    else:
        return obj


async def serve(uri: str, username: str, password: str, database: str = "neo4j") -> None:
    """启动Neo4j MCP服务器"""
    logger.info("正在启动Neo4j MCP服务器")
    server = Server("mcp-neo4j")
    neo4j_server = Neo4jServer(uri, username, password, database)
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """列出可用的Neo4j工具"""
        logger.info("列出可用工具")
        return [
            Tool(
                name=Neo4jTools.RUN_QUERY.value,
                description="执行Cypher查询语句",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Cypher查询语句",
                        },
                        "parameters": {
                            "type": "object",
                            "description": "查询参数（可选）",
                        }
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name=Neo4jTools.GET_DATABASE_INFO.value,
                description="获取Neo4j数据库信息，包括版本、节点数量、关系数量等",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name=Neo4jTools.GET_NODE_LABELS.value,
                description="获取数据库中所有节点标签",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name=Neo4jTools.GET_RELATIONSHIP_TYPES.value,
                description="获取数据库中所有关系类型",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name=Neo4jTools.GET_NODE_PROPERTIES.value,
                description="获取指定标签节点的属性信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "label": {
                            "type": "string",
                            "description": "节点标签名称",
                        }
                    },
                    "required": ["label"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """处理Neo4j工具调用"""
        try:
            logger.info(f"调用工具: {name}, 参数: {arguments}")
            result = None
            match name:
                case Neo4jTools.RUN_QUERY.value:
                    query = arguments.get("query")
                    if not query:
                        raise ValueError("缺少必要参数: query")
                    parameters = arguments.get("parameters", {})
                    result = await neo4j_server.run_query(query, parameters)

                case Neo4jTools.GET_DATABASE_INFO.value:
                    result = neo4j_server.get_database_info()

                case Neo4jTools.GET_NODE_LABELS.value:
                    labels = neo4j_server.get_node_labels()
                    result = {"labels": labels}

                case Neo4jTools.GET_RELATIONSHIP_TYPES.value:
                    types = neo4j_server.get_relationship_types()
                    result = {"relationship_types": types}

                case Neo4jTools.GET_NODE_PROPERTIES.value:
                    label = arguments.get("label")
                    if not label:
                        raise ValueError("缺少必要参数: label")
                    properties = neo4j_server.get_node_properties(label)
                    result = {"label": label, "properties": properties}

                case _:
                    raise ValueError(f"未知工具: {name}")

            serialized_result = serialize_neo4j_obj(result.model_dump() if hasattr(result, "model_dump") else result)
            logger.info("工具调用成功")
            return [
                TextContent(type="text", text=json.dumps(
                    serialized_result,
                    ensure_ascii=False,
                    indent=2
                ))
            ]

        except Exception as e:
            logger.error(f"工具调用失败: {str(e)}")
            raise ValueError(f"处理Neo4j查询时出错: {str(e)}")

    options = server.create_initialization_options()
    logger.info("Neo4j MCP服务器启动成功")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
