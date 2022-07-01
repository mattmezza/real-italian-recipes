import readline
import os
import json
from functools import partial
from operator import contains
from pathlib import Path

with open(Path(__file__).parent / "book.json", "r") as f:
    book = json.load(f)


def rprint(r):
    should_go_back = False
    c = None
    while should_go_back is False:
        if c is None:
            print("-" * 40)
            print(
                "{} ({}min) {}".format(
                    r["title"],
                    int(r["total_time"]) if r["total_time"] else "-",
                    ("+" * int(r["ratings"])).ljust(5, "-") if r["ratings"] else "",
                )
            )
            print("Recipe for {}\n".format(r["yields"]))
            print("Ingredients:")
            print("- " + "\n- ".join(r["ingredients"]))
            print("-" * 40)

        c = input("Enter -> back, 'i' -> instructions, 'p' -> photo 'm' -> see more: ")
        if c == "i":
            print("Instructions:")
            print(r["instructions"])
        elif c == "p":
            os.system("open {}".format(r["image"]))
        elif c == "m":
            os.system("open {}".format(r["url"]))
        else:
            should_go_back = True


def rprintall(rr):
    if len(rr) == 0:
        print("No res")
    for r in rr:
        rprint(r)


def by_ingr(ingr, criterion):
    res = []
    for u, r in book.items():
        if criterion(ingr, r["ingredients"]):
            r["url"] = u
            res.append(r)
    return res


def cr_all(qingr, ringr):
    return all(
        map(
            partial(contains, " ".join(ringr).lower()),
            qingr,
        )
    )


def cr_any(qingr, ringr):
    return any(
        map(
            partial(contains, " ".join(ringr).lower()),
            qingr,
        )
    )


def cr_complete(qingr, ringr):
    return all(
        [
            any([q.lower() in i for q in qingr])
            for i in [i.lower() for i in ringr]
        ]
    )


def print_res(res):
    if len(res) == 0:
        print("No res")
        return
    should_go_back = False
    while should_go_back is False:
        for i, r in enumerate(res):
            print("{:>3}: {:.60}".format(i, r["title"]))

        r = input("\nEnter number to see details: ")
        if r == "b" or r == "" or any(map(lambda x: x not in "0123456789", r)):
            should_go_back = True
        else:
            rprint(res[int(r)])


def help():
    print("available cmd: 'i' 'iany' 'iall' 't' 'q'")


def by_title(tt):
    res = []
    for u, r in book.items():
        if any(map(partial(contains, r["title"].lower()), tt)):
            r["url"] = u
            res.append(r)
    return res



if __name__ == "__main__":
    help()
    should_exit = False
    while should_exit is False:
        i = input()
        by, *what = i.split(" ")
        if by == "i" or by == "ingr":
            print_res(by_ingr(what, cr_complete))
            help()
        elif by == "iall" or by == "ingrall":
            print_res(by_ingr(what, cr_all))
            help()
        elif by == "iany" or by == "ingrany":
            print_res(by_ingr(what, cr_any))
            help()
        elif by == "t" or by == "title":
            print_res(by_title(what))
            help()
        elif by == "q":
            should_exit = True
        elif by == "":
            print()
        else:
            help()
    if should_exit:
        print('bye')

