from typing import List
from db_definition import Manga, Episode
from uuid import uuid4


def identify_episodes(episodes: List[Episode]):
    """helper function to parse ep_l_name, ep_l_link, ep_c_name, ep_c_link
    if found in given episodes."""
    ep_l_id, ep_l_name, ep_l_link, ep_c_id, ep_c_name, ep_c_link = (
        "",
        "",
        "",
        "",
        "",
        "",
    )
    for ep in episodes:
        match ep.episode_tag:
            case "l":
                ep_l_id = ep.episode_id
                ep_l_name = ep.episode_name
                ep_l_link = ep.episode_link
            case "c":
                ep_c_id = ep.episode_id
                ep_c_name = ep.episode_name
                ep_c_link = ep.episode_link

    return ep_l_id, ep_l_name, ep_l_link, ep_c_id, ep_c_name, ep_c_link
