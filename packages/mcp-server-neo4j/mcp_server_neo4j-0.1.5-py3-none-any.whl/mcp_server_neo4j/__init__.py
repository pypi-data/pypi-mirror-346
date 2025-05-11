from .server import serve


def main():
    """MCP Neo4j Server - Neo4j 数据库操作功能服务"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="提供Neo4j数据库操作功能的MCP服务器"
    )
    parser.add_argument("--uri", type=str, default="bolt://localhost:7687", help="Neo4j数据库URI")
    parser.add_argument("--username", type=str, default="neo4j", help="Neo4j用户名")
    parser.add_argument("--password", type=str, help="Neo4j密码")
    parser.add_argument("--database", type=str, default="neo4j", help="Neo4j数据库名称")

    args = parser.parse_args()
    asyncio.run(serve(args.uri, args.username, args.password, args.database))

if __name__ == "__main__":
    main()