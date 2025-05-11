"""
In this module we handle the server information
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from .utils import SAMPQuery_Encodings, SAMPQuery_Utils


@dataclass
class SAMPQuery_Server:
    """
    This class represents the server information

    :param str name: The name of the server
    :param bool password: If the server has a password
    :param int players: The number of players
    :param int max_players: The maximum number of players
    :param str gamemode: The gamemode of the server (e.g DM, TDM, etc.)
    :param str language: The language of the server
    """

    name: str
    password: bool
    players: int
    max_players: int
    gamemode: str
    language: str
    encodings: SAMPQuery_Encodings

    @classmethod
    def from_data(cls, data: bytes) -> SAMPQuery_Server:
        """
        Create an instance of server from raw byte data.

        :param bytes data: The raw data to parse into server information.
        :return SAMPQuery_Server: An instance of SAMPQuery_Server with the parsed data.
        """
        password, players, max_players = struct.unpack_from("<?HH", data)
        data = data[5:]
        name, data, name_encoding = SAMPQuery_Utils.unpack_string(data, "I")
        gamemode, data, gamemode_encoding = SAMPQuery_Utils.unpack_string(data, "I")
        language, data, language_encoding = SAMPQuery_Utils.unpack_string(data, "I")
        assert not data
        return cls(
            name=name,
            password=password,
            players=players,
            max_players=max_players,
            gamemode=gamemode,
            language=language,
            encodings=dict(
                name=name_encoding,
                gamemode=gamemode_encoding,
                language=language_encoding,
            ),
        )
