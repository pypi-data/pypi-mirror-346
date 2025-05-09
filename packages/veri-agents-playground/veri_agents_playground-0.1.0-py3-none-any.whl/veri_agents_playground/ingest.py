import argparse
import logging

from hydra import compose, initialize

from veri_agents_playground.agents.knowledgebase import Knowledgebase
from veri_agents_playground.agents.system import init_from_config
from veri_agents_playground.schema.schema import DataSource

# set logging basicConfig so that it doesn't show httpx messages and also shows date and time
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)


def parse_args():
    parser = argparse.ArgumentParser(description="Knowledgebase indexing")
    parser.add_argument(
        "--kb", type=str, required=True, help="Name of the knowledge base to index"
    )
    parser.add_argument(
        "--dsl",
        type=str,
        required=False,
        help="Location of the data source, e.g. a file path or URL.",
    )
    parser.add_argument(
        "--dsn",
        type=str,
        required=False,
        help="Name of the data source. Can be used for filtering in the knowledgebase and important that document names are unique",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        required=False,
        help="Incremental indexing",
    )
    parser.add_argument(
        "--tags",
        type=str,
        required=False,
        help="Tags applied to all documents and chunks of the source, e.g. 'finance,high_priority'.",
    )
    parser.set_defaults(incremental=False)
    return parser.parse_args()


def main():
    args = parse_args()
    with initialize(
        version_base=None, config_path="./conf", job_name="veritone_ingest"
    ):
        cfg = compose(config_name="config")
        init_from_config(cfg)

    kb = Knowledgebase.get_knowledgebase(args.kb)
    if kb is None:
        print(
            f"Knowledgebase not found, available knowledgebases: {Knowledgebase.knowledge_bases.keys()}"
        )
        return

    # Data source provided from command-line
    if args.dsl and args.dsn:
        tags = []
        # parse tags into dict from tag1_key:tag1_value,tag2_key:tag2_value
        try:
            tags = [tag for tag in args.tags.split(",")]
        except Exception:
            print("Error parsing tags, example format: 'finance,priority_high'")
            return
        ds = DataSource(
            location=args.dsl, name=args.dsn, incremental=args.incremental, tags=tags
        )
        kb.index(ds)
    # Otherwise use the data sources defined in the config
    else:
        kb.index()


if __name__ == "__main__":
    main()
