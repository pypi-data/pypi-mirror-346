# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
import base64
import binascii
from urllib.parse import urlparse


def build_badge_part(instance: str, pid: int, sid: int) -> str | None:
    """
    build a badge part value

    Builds a badge part value based on an instance URL, project identifier and
    scheduled task identifier. This is to help provide a user a string
    which that can use for image requests that contain all the information
    needed for this tool to make an API request with a configured GitLab
    instance (in combination with the runtime configuration).

    Args:
        instance: the instance of the gitlab entity
        pid: the project identifier holding the scheduled task
        sid: the scheduled task identifier

    Returns:
        tuple of an instance, project identifier or scheduled task identifier
        the badge part to decode
    """

    # a bit of protection to avoid use from building a part that should not
    # exist
    if not instance or not pid or pid < 0 or not sid or sid < 0:
        return None

    # we strip out the schemap and trailing slash, as we do not needed to
    # include this in the badge identifier
    parsed = urlparse(instance)
    shorter_instance = parsed.geturl()[len(parsed.scheme) + 3:].strip('/')

    # if this was not https, add a hint that we can use when decoding to
    # re-apply the http scheme
    if parsed.scheme == 'http':
        shorter_instance = f'!{shorter_instance}'

    # encode pid/sid values into 4-byte fields to be a smaller identifier
    # (four bytes should be enough; right?)
    try:
        pid_data = pid.to_bytes(4, byteorder='big')
        sid_data = sid.to_bytes(4, byteorder='big')
    except OverflowError:
        return None

    try:
        encoded_instance = shorter_instance.encode('utf-8')
    except UnicodeEncodeError:
        return None

    parts = [
        pid_data,
        sid_data,
        encoded_instance,
    ]

    try:
        return base64.urlsafe_b64encode(b''.join(parts)).decode('ascii')
    except binascii.Error:
        return None


def decode_badge_part(value: bytes | str) -> tuple[str, int, int] | None:
    """
    decode a badge part value

    Decodes a badge part value into an instance URL, project identifier and
    scheduled task identifier. See ``build_badge_part`` for more information.

    Args:
        value: the badge part to decode

    Returns:
        tuple of an instance, project identifier or scheduled task identifier
    """

    try:
        raw_decoded = base64.urlsafe_b64decode(value)
    except binascii.Error:
        return None

    MIN_LEN = 4 + 4 + 2  # pid:4, sid:4, domain:>=2  noqa: N806
    if len(raw_decoded) < MIN_LEN:
        return None

    pid_data = raw_decoded[0:4]
    sid_data = raw_decoded[4:8]
    encoded_instance = raw_decoded[8:]

    pid = int.from_bytes(pid_data, byteorder='big')
    sid = int.from_bytes(sid_data, byteorder='big')

    try:
        instance = encoded_instance.decode()
    except UnicodeDecodeError:
        return None

    instance = instance.strip()
    if not instance:
        return None

    if instance.startswith('!'):
        final_instance = f'http://{instance[1:]}/'
    else:
        final_instance = f'https://{instance}/'

    return final_instance, pid, sid
