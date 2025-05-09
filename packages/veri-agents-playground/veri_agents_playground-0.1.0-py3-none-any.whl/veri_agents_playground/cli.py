from omegaconf import DictConfig, OmegaConf
import hydra

from veri_agents_playground.agents import init_from_config
from veri_agents_playground.agents.workflow import Workflow


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))

    init_from_config(cfg)
    wf = Workflow.get_workflow("veritone_agent")
    if wf is None:
        print(f"Workflow not found: {cfg.workflow.name}, available workflows: {Workflow.get_workflows().keys()}")
        return
    #answer = wf.invoke("Please find me a video of Serena Williams playing tennis.")
    answer = wf.invoke("what should I do if my DMH file is unplayable?")
    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    main()
