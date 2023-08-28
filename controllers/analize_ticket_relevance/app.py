from modules.get_response_from_prompt import get_response_from_prompt
from modules.send_message import send_message_to_user
import re


async def analize_ticket_relevance(
    ticket_id, original_comment, modified_body, all_addressed_persons
):
    print(all_addressed_persons, len(all_addressed_persons))
    relevance_scores = []
    # for person in all_addressed_persons:
    print(
        f"""Assign a relevance scores from 1 to 5 for these {all_addressed_persons} in the JIRA comment based on relevance of comment to him/her: {modified_body}.
        Give cc'd person a score always less than 4. Don't provide any explanation or logic behind scoring. Put the assigned score in an python list
        and just display the list at the end. The list should be in the same order as the people tagged. For example, output should be like this: [5,3] for two people tagged.
        .
        """
    )
    relevance_score_string = get_response_from_prompt(
        f"""Assign a relevance scores from 1 to 5 for these {all_addressed_persons} in the JIRA comment based on relevance of comment to him/her: {modified_body}.
        Give cc'd person a score always less than 4. Don't provide any explanation or logic behind scoring. Put the assigned score in an python list
        and just display the list at the end. The list should be in the same order as the people tagged. For example, output should be like this: [5,3] for two people tagged.
        .
        """
    )

    score_pattern = re.compile(r"\[(\d+,\d+)\]")
    match = score_pattern.search(relevance_score_string)
    if match:
        relevance_scores = list(map(int, match.group(1).split(",")))
        print("scores___________________________", relevance_scores)
    else:
        default_scores = [3] * len(all_addressed_persons)
        print("default_scores", default_scores)

    # print("relevance_score", relevance_score_string)
    # parse the relevance_score_string -> list
    # assign to relevance_scores
    print(len(all_addressed_persons), len(relevance_scores))
    for i in range(len(all_addressed_persons)):
        person = all_addressed_persons[i]
        relevance_score = relevance_scores[i]
        if relevance_score >= 4:
            await send_message_to_user(
                person, message=f"{ticket_id}:{original_comment}", blocks=[]
            )
