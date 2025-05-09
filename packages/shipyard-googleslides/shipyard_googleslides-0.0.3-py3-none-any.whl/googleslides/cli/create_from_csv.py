import argparse
import os
import openai

import pandas as pd

from .create_from_yaml import create_presentation_from_yaml
from shipyard_templates import ShipyardLogger

logger = ShipyardLogger.get_logger()

# consts for chatgpt
number_of_responses = 1
randomness = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file_name",
        help="The input data to generate content about in csv format",
        required=True,
    )
    parser.add_argument(
        "--base_prompt",
        help="Basic instructions for chatgpt to follow. This will be appended to the template prompt.",
        required=True,
    )
    parser.add_argument(
        "--output_file_name",
        help="The output file name, saved to disk. Defaults to slide_content.txt",
        default="slide_content.txt",
        required=False,
    )
    parser.add_argument(
        "--service-account",
        dest="gcp_application_credentials",
        default=None,
        required=False,
    )
    return parser.parse_args()


def generate_slide_yaml(df: pd.DataFrame, base_prompt: str) -> str:
    """Generates slide content in YAML format based on the provided data and base prompt."""
    try:
        key = os.environ["CHATGPT_API_KEY"]
    except KeyError:
        raise KeyError(
            "CHATGPT_API_KEY environment variable is not set. Make sure your credentials are correctly selected."
        )
    openai.api_key = key

    if df.empty:
        raise ValueError(
            f"No data found in the sheet {args.sheet_name}, {args.sheet_id}."
        )

    prompt = f"""
    You are a helpful assistant that generates slide content based on the provided data.
    
    Your client has asked you to follow these instructions:
    {base_prompt}
    
    Given the following data, please create a slide content outline. The data is in the format of a table with columns: {', '.join(df.columns)}. The data is as follows:
    
    {df.to_string(index=False)}
    
    Provide slide content in YAML format. Data should be structured like the following example:
    
    ```
    title: "Quarterly Business Review"

    slides:
      - title: "Welcome & Agenda"
        body: |
          Welcome to the QBR.
          In this presentation:
          - We will recap Q2 performance
          - Discuss key wins and challenges
          - Review goals for next quarter

      - title: "Key Metrics"
        body: |
          - Revenue: $2.3M (↑12%)
          - Conversion Rate: 4.5% (↑0.3%)
          - Customer Retention: 89%

      - title: "Top Performing Campaigns"
        body: |
          1. Summer Sale - ROAS 8.1
          2. Back-to-School - ROAS 6.4
          3. New Arrivals - ROAS 5.9

      - title: "Challenges Faced"
        body: |
          - Rising customer acquisition costs
          - Attribution gaps across channels
          - Limited performance on TikTok

      - title: "Next Steps"
        body: |
          ✅ Launch loyalty program by next quarter
          ✅ Optimize ad spend across Google & Meta
          ✅ Improve campaign attribution with enhanced tracking

      - title: "Thank You"
        body: |
          Questions? Feedback?
          Let's discuss how we can grow together!
    ```
    
    Rules for generation:
    1. Provide only the slide content in valid YAML, without any additional explanations or comments.
    2. Ensure you provide sufficient body content for each slide. Slides shouldn't be too concise.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        n=number_of_responses,
        temperature=randomness,
        messages=[{"role": "user", "content": prompt}],
    )
    logger.debug(f"Completion response: {completion}")

    slide_content = completion.choices[0].message.content
    return slide_content

def main():
    args = parse_args()

    df = pd.read_csv(args.input_file_name)
    slide_yaml = generate_slide_yaml(df, args.base_prompt)

    # output the response to a new file
    output_file = args.output_file_name
    with open(output_file, "w") as f:
        f.write(slide_yaml)

    service_account = args.gcp_application_credentials
    create_presentation_from_yaml(output_file, service_account)



if __name__ == "__main__":
    main()