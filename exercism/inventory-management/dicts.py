from collections import Counter
from operator import inv

def create_inventory(items):
    """

    :param items: list - list of items to create an inventory from.
    :return:  dict - the inventory dictionary.
    """

    return dict(Counter(items))


def add_items(inventory, items):
    """

    :param inventory: dict - dictionary of existing inventory.
    :param items: list - list of items to update the inventory with.
    :return:  dict - the inventory dictionary update with the new items.
    """

    new_list = []

    for k, v in inventory.items():
        for i in range(v):
            new_list.append(k)
    return create_inventory(new_list + items)



def decrement_items(inventory, items):
    """

    :param inventory: dict - inventory dictionary.
    :param items: list - list of items to decrement from the inventory.
    :return:  dict - updated inventory dictionary with items decremented.
    """

    new_items = create_inventory(items)

    for k, v in inventory.items():
        if (inventory[k] - new_items[k]) < 0:
            inventory[k] = 0
        else:
            inventory[k] -= new_items[k]
    
    return inventory


def remove_item(inventory, item):
    """
    :param inventory: dict - inventory dictionary.
    :param item: str - item to remove from the inventory.
    :return:  dict - updated inventory dictionary with item removed.
    """

    try:
        del inventory[item]
    except KeyError:
        None
    return inventory


def list_inventory(inventory):
    """

    :param inventory: dict - an inventory dictionary.
    :return: list of tuples - list of key, value pairs from the inventory dictionary.
    """

    return [(k, v) for k, v in inventory.items() if v > 0]
