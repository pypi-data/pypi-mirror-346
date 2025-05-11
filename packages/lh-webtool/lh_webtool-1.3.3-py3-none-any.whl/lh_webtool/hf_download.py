# -*- encoding: utf-8 -*-
"""
@File    :   hf_download.py
@Time    :   2024/10/31 15:26:42
@Author  :   lihao57
@Version :   1.0
@Contact :   lihao57@baidu.com
@Reference:  https://github.com/LetheSec/HuggingFace-Download-Accelerator/blob/main/hf_download.py
"""


import os
import sys
import time
import logging
import argparse
import huggingface_hub


def download(
    args,
):
    """ """
    if args.use_hf_transfer:
        import hf_transfer

        # Enable hf-transfer if specified
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        logging.info(
            "export HF_HUB_ENABLE_HF_TRANSFER={}".format(
                os.getenv("HF_HUB_ENABLE_HF_TRANSFER")
            )
        )

    if args.model is None and args.dataset is None:
        logging.error("No model or dataset was specified.")
        sys.exit()
    elif args.model is not None and args.dataset is not None:
        logging.error("Only one model or dataset can be downloaded at a time.")
        sys.exit()

    if args.use_mirror:
        # Set default endpoint to mirror site if specified
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        logging.info("export HF_ENDPOINT={}".format(os.getenv("HF_ENDPOINT")))

    if args.token is not None:
        token_option = f"--token {args.token}"
    else:
        token_option = ""

    if args.include is not None:
        include_option = f"--include {args.include}"
    else:
        include_option = ""

    if args.exclude is not None:
        exclude_option = f"--exclude {args.exclude}"
    else:
        exclude_option = ""

    options = args.options if args.options is not None else ""

    if args.model is not None:
        if args.save_dir is not None:
            save_path = os.path.join(args.save_dir, args.model)
            save_dir_option = f"--local-dir {save_path}"
        else:
            save_dir_option = ""

        download_shell = f"huggingface-cli download {token_option} {include_option} {exclude_option} {options} --repo-type model {args.model} {save_dir_option}"
        logging.info(download_shell)
        os.system(download_shell)

    elif args.dataset is not None:
        if args.save_dir is not None:
            save_path = os.path.join(args.save_dir, args.dataset)
            save_dir_option = f"--local-dir {save_path}"
        else:
            save_dir_option = ""

        download_shell = f"huggingface-cli download {token_option} {include_option} {exclude_option} {options} --repo-type dataset {args.dataset} {save_dir_option}"
        logging.info(download_shell)
        os.system(download_shell)


def main():
    # set base logging config
    fmt = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s] %(message)s"
    logging.basicConfig(format=fmt, level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="HuggingFace Download Accelerator Script."
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="model name in huggingface, e.g., baichuan-inc/Baichuan2-7B-Chat",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        type=str,
        help="dataset name in huggingface, e.g., zh-plus/tiny-imagenet",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="hugging face access token for download meta-llama/Llama-2-7b-hf, e.g., hf_***** ",
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        help="Specify the file to be downloaded",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        help="Files you don't want to download",
    )
    parser.add_argument(
        "-o",
        "--options",
        type=str,
        help="Other options",
    )
    parser.add_argument(
        "--save_dir",
        "-s",
        type=str,
        help="path to be saved after downloading.",
    )
    parser.add_argument(
        "--use_hf_transfer",
        default=True,
        type=eval,
        help="Use hf-transfer, default: True",
    )
    parser.add_argument(
        "--use_mirror",
        default=True,
        type=eval,
        help="Download from mirror, default: True",
    )
    args = parser.parse_args()
    logging.info(args)

    t1 = time.time()

    # run
    download(args)

    t2 = time.time()
    logging.info("time: {}".format(t2 - t1))


if __name__ == "__main__":
    main()
