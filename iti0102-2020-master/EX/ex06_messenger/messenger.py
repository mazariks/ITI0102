"""Messenger."""


class User:
    """User class."""

    def __init__(self, name):
        """
        User constructor.

        :param name: Name of the user.
        """
        self.name = name


class Chat:
    """Chat class."""

    def __init__(self, name, users):
        """
        Chat constructor.

        :param name: Name of the chat.
        :param users: Users in the chat.
        """
        self.name = name
        self.users = users
        self.messages = []


class Message:
    """Message class."""

    def __init__(self, user, content):
        """
        Message constructor.

        :param user: Author of the message.
        :param content: Content of the message.
        """
        self.user = user
        self.content = content
        self.reactions = 0


def write_message(user: User, chat: Chat, content: str) -> None:
    """
    Write a message to given chat.

    Create a message with given values and then add it to the chat's messages.

    :param user: Author of the message.
    :param chat: Chat to write the message to.
    :param content: Content of the message.
    """
    message = Message(user, content)
    if message.user in chat.users:
        chat.messages.append(message)


def delete_message(chat: Chat, message: Message) -> None:
    """
    Delete message from chat.

    :param chat: Chat to delete message from.
    :param message: Message to delete from chat.
    """
    if message in chat.messages:
        chat.messages.remove(message)


def get_messages_by_user(user: User, chat: Chat) -> list:
    """
    Get messages by user in chat.

    :param user: User whose messages to get.
    :param chat: Chat from where to get user's messages.
    :return: A list of messages.
    """
    list_of_messages = []
    for x in chat.messages:
        if x.user == user:
            list_of_messages.append(x)
    return list_of_messages


def react_to_last_message(chat: Chat) -> None:
    """
    Add reaction to last message in chat.

    :param chat: Chat in which the message is.
    """
    if len(chat.messages) != 0:
        chat.messages[-1].reactions += 1


def find_most_reacted_message(chat: Chat) -> Message:
    """
    Find the most reacted message in chat.

    :param chat: Chat to get the message from.
    :return: Most reacted message.
    """
    message_to_return = object
    reactions_counter = 0
    for x in chat.messages:
        if x.reactions >= reactions_counter:
            reactions_counter = x.reactions
            message_to_return = x
    return message_to_return


def count_reactions_in_chat(chat: Chat) -> int:
    """
    Count all reactions in chat.

    :param chat: Said chat.
    :return: The amount of reactions.
    """
    reactions_counter = 0
    for x in chat.messages:
        reactions_counter += x.reactions
    return reactions_counter


def count_reactions_by_chat(chats: list) -> dict:
    """
    Count reactions in every chat.

    The function should return a dict where the key is the name of a chat and the value is the amount of reactions.

    :param chats: The chats in question.
    :return: A dictionary as described.
    """
    dictionary = {}
    for chat in chats:
        reactions_of_chat = count_reactions_in_chat(chat)
        if reactions_of_chat in dictionary.values():
            dictionary[chat.name] += reactions_of_chat
        else:
            dictionary[chat.name] = reactions_of_chat
    return dictionary


if __name__ == "__main__":
    # Users
    user1 = User("Teet")
    user2 = User("Tiit")
    user3 = User("User3")
    user4 = User("User4")

    # Chats
    chat1 = Chat("Chat1", [user1, user2])
    chat2 = Chat("Chat2", [user3, user4])
    chats = [chat1, chat2]

    # Write messages and react
    write_message(user1, chat1, "user1 Message1")
    react_to_last_message(chat1)
    write_message(user2, chat1, "user2 Message2")
    for _ in range(69):
        react_to_last_message(chat1)
    write_message(user1, chat1, "user1 Message3")
    write_message(user4, chat2, "Hello")
    write_message(user3, chat2, "Delete me")
    write_message(user4, chat2, "World")
    delete_message(chat2, chat2.messages[1])
    write_message(user3, chat1, "Why my message is here? I'm not in user list")

    # write and delete messages
    print([message.content for message in chat1.messages])  # ['user1 Message1', 'user2 Message2', 'user1 Message3']
    print([message.content for message in chat2.messages])  # ['Hello', 'World']

    # get_messages_by_user
    print([message.content for message in get_messages_by_user(user1, chat1)])  # ['user1 Message1', 'user1 Message3']

    # React to last
    print(f"Before reaction: {chat2.messages[-1].reactions}")  # 0
    react_to_last_message(chat2)
    print(f"After reaction: {chat2.messages[-1].reactions}")  # 1

    # Test same reaction nums
    print(find_most_reacted_message(chat1).content)  # user2 Message2
    for _ in range(69):
        react_to_last_message(chat1)
    print(find_most_reacted_message(chat1).content)  # user1 Message3
    print(count_reactions_in_chat(chat1))  # 139

    # Count reactions by chat
    print(count_reactions_by_chat(chats))  # {'Chat1': 139, 'Chat2': 1
