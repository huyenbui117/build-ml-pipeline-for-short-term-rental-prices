#!/usr/bin/env python
"""
Download from W&B raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    df = pd.read_csv(artifact_local_path)

    # Drop duplicates
    logger.info("Dropping duplicates")
    df = df.drop_duplicates()

    # Drop outliers
    logger.info("Dropping outliers")
    logger.info(f"Number of examples before: {len(df)}")
    df = df[df.price.between(args.min_price, args.max_price)].reset_index(drop=True)
    logger.info(f"Number of examples after: {len(df)}")

    # Convert last_review to datetime
    logger.info("Converting last_review to datetime")
    df["last_review"] = pd.to_datetime(df.last_review)

    # Save cleaned dataframe to new artifact
    logger.info("Saving cleaned dataframe to new artifact")
    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    artifact.add_file(args.output_artifact)

    # Log artifact to W&B
    logger.info("Logging artifact")
    run.log_artifact(artifact)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Path to the input artifact from W&B",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price of the cars to be analyzed",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price of the cars to be analyzed",
        required=True
    )

    args = parser.parse_args()

    go(args)
