from modules.get_response_from_prompt import get_response_from_prompt
from modules.send_message import send_message_to_user


async def analize_ticket_relevance(
    ticket_id, original_comment, modified_body, all_addressed_persons
):
    for person in all_addressed_persons:
        relevance_score = get_response_from_prompt(
            f"""Assign an relevance scores for all the tagged individuals in the JIRA comment based on relevance to them: {modified_body}.
            Give cc'd person less importance. Provide score of each person on a new line. The new line should always start with -----."""
        )
        print("relevance_score", relevance_score)
        if relevance_score > 4:
            send_message_to_user(
                person, message=f"{ticket_id}:{original_comment}", blocks=[]
            )