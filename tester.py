# import ast

# a = "asd"


# class ObfuscatorError(RuntimeError): ...


# try:
#     raise ObfuscatorError("asd")
# except ObfuscatorError as e:
#     if e.args != ("asd",):
#         print("ObfuscatorError raise error")
#     else:
#         print("raise test passed")


# def nigger(d: str):
#     global a
#     a = a + d


# def loader():
#     global asd
#     asd = "asd32"


# class Pidr:
#     nigger("3")
#     xxx = 123


# def closu():
#     loader()
#     g = "a"

#     def pidr(d: str):
#         nonlocal g
#         g = g + d
#         match d:
#             case "sd":
#                 g += str(3)

#     nigger("2")
#     pidr("sd")
#     pidr("2")
#     if not (a == g == asd):
#         print("nonlocal/global + const error")
#     else:
#         print("nonlocal/global + const test passed!")


# def cefefe():
#     a = 0
#     for asd in range(100):
#         if asd % 2 == 0:
#             continue
#         elif (asd + 1) % 16 == 0:
#             break

#         a += asd
#     if a != 49:
#         print("break/continue error")
#     else:
#         print("break/continue passed")

#     a1 = 0
#     for asd in range(100):
#         try:
#             if asd % 2 == 0:
#                 try:
#                     continue
#                 except:
#                     pass
#             elif (asd + 1) % 16 == 0:
#                 try:
#                     break
#                 except BaseException:
#                     pass
#         except:
#             pass
#         a1 += asd
#     if a1 != 49:
#         print("break/continue (try except) error")
#     else:
#         print("break/continue (try except) passed")


# def kwtest():

#     def a_cell(id):
#         return [id]

#     c_a = a_cell(id="asd")
#     c_n = ast.Name(id="asd")
#     if c_a[0] != c_n.id:
#         print("kw args test 1 error!")
#     else:
#         print("kw args test 1 passed!")

#     # ращница в том что id - имя из builtin, а arg нет

#     def b_cell(arg):
#         return [arg]

#     c_a = b_cell(arg="asd")
#     c_n = ast.arg(arg="asd")
#     if c_a[0] != c_n.arg:
#         print("kw args test 2 error!")
#     else:
#         print("kw args test 2 passed!")


# def attrer():
#     class Attrst:
#         arg = "123"
#         other = 123
#         value = "asd"

#         def nig(sel_f):
#             return "as" + sel_f.forv()

#         def forv(s_elf):
#             return "sa"

#         @staticmethod
#         def X():
#             return "sa" + Attrst().nig()

#     def giga(x):
#         return x.value

#     if giga(ast.Constant("asd")) == giga(Attrst):
#         print("attr test 1 passed!")
#     else:
#         print("attr test 1 error!")

#     if Pidr.xxx == 123 == Attrst.other:
#         print("attr test 2 passed!")
#     else:
#         print("attr test 2 error!")

#     if Attrst.X() == "saassa":
#         print("attr test 3 passed!")
#     else:
#         print("attr test 3 error!")


# def sideff():
#     from types import SimpleNamespace

#     cnt = 0

#     def flag(x):
#         nonlocal cnt
#         cnt += x
#         return cnt

#     def test(x=SimpleNamespace(c=1)):
#         flag(x.c)
#         return x

#     test().c += 1
#     test().c += 1

#     res1 = test()
#     if cnt != 6:
#         print("side effect test 1 error!")
#     else:
#         print("side effect test 1 passed!")

#     if str(res1) != "namespace(c=3)":
#         print("side effect test 2 error!")
#     else:
#         print("side effect test 2 passed!")

#     if [test(), cnt][1] != 9:
#         print("side effect test 3 error!")
#     else:
#         print("side effect test 3 passed!")


# def deltest():
#     x = 10
#     del x
#     try:
#         x
#         print("del test 1 (local) error!")
#     except NameError:
#         print("del test 1 (local) passed!")

#     class Holder:
#         def __init__(self):
#             self.val = 5

#         def drop(self):
#             del self.val

#     h = Holder()
#     h.drop()
#     if hasattr(h, "val"):
#         print("del test 2 (attr) error!")
#     else:
#         print("del test 2 (attr) passed!")

#     p = q = 1
#     del p, q
#     try:
#         q
#         print("del test 3 (tuple) error!")
#     except NameError:
#         print("del test 3 (tuple) passed!")


# def statictest():
#     class Box:
#         def __init__(self):
#             self.size = 0

#         def grow(self):
#             self.size += 1

#     class Tool:
#         @staticmethod
#         def read(src):
#             return src.size  # src - внешний объект, .size не self и не должен переименовываться

#     from types import SimpleNamespace

#     ns = SimpleNamespace()
#     setattr(ns, "size", 123)

#     b = Box()
#     b.grow()
#     if Tool.read(ns) == 123 and b.size == 1:
#         print("staticmethod test passed!")
#     else:
#         print("staticmethod test error!")


# def kwclstest():
#     class A:
#         def run(self, val=1):
#             return ("A", val)

#     class B:
#         def run(self, val=2):  # то же имя метода и тот же kwarg, что у A
#             return ("B", val)

#     if A().run(val=10) == ("A", 10) and B().run(val=20) == ("B", 20):
#         print("kw cls test 1 (method collision) passed!")
#     else:
#         print("kw cls test 1 (method collision) error!")

#     class Cfg:
#         def __init__(self, factor=2, label="x"):
#             self.factor = factor
#             self.label = label

#     c = Cfg(factor=5, label="y")
#     if c.factor == 5 and c.label == "y":
#         print("kw cls test 2 (ctor kwargs) passed!")
#     else:
#         print("kw cls test 2 (ctor kwargs) error!")

#     class BaseC:
#         def __init__(self, items):
#             self.items = items

#     class SubC(BaseC): ...

#     if SubC(items=[1, 2, 3]).items == [1, 2, 3]:
#         print("kw cls test 3 (inherited ctor) passed!")
#     else:
#         print("kw cls test 3 (inherited ctor) error!")


# if __name__ == "__main__":
#     closu()
#     cefefe()
#     kwtest()
#     attrer()
#     sideff()

#     # new
#     deltest()
#     statictest()
#     kwclstest()



# link to the file: https://t.me/PaketPKSoftware
# link to the file: https://t.me/PaketPKSoftware
# link to the file: https://t.me/PaketPKSoftware
# link to the file: https://t.me/PaketPKSoftware

import ast

a = "asd"


class ObfuscatorError(RuntimeError): ...


try:
    raise ObfuscatorError("asd")
except ObfuscatorError as e:
    if e.args != ("asd",):
        print("ObfuscatorError raise error")
    else:
        print("raise test passed")


def nigger(d: str):
    global a
    a = a + d


def loader():
    global asd
    asd = "asd32"


class Pidr:
    nigger("3")
    xxx = 123


def closu():
    loader()
    g = "a"

    def pidr(d: str):
        nonlocal g
        g = g + d
        match d:
            case "sd":
                g += str(3)

    nigger("2")
    pidr("sd")
    pidr("2")
    if not (a == g == asd):
        print("nonlocal/global + const error")
    else:
        print("nonlocal/global + const test passed!")


def cefefe():
    a = 0
    for asd in range(100):
        if asd % 2 == 0:
            continue
        elif (asd + 1) % 16 == 0:
            break

        a += asd
    if a != 49:
        print("break/continue error")
    else:
        print("break/continue passed")

    a1 = 0
    for asd in range(100):
        try:
            if asd % 2 == 0:
                try:
                    continue
                except:
                    pass
            elif (asd + 1) % 16 == 0:
                try:
                    break
                except BaseException:
                    pass
        except:
            pass
        a1 += asd
    if a1 != 49:
        print("break/continue (try except) error")
    else:
        print("break/continue (try except) passed")


def kwtest():

    def a_cell(id):
        return [id]

    c_a = a_cell(id="asd")
    c_n = ast.Name(id="asd")
    if c_a[0] != c_n.id:
        print("kw args test 1 error!")
    else:
        print("kw args test 1 passed!")

    # ращница в том что id - имя из builtin, а arg нет

    def b_cell(arg):
        return [arg]

    c_a = b_cell(arg="asd")
    c_n = ast.arg(arg="asd")
    if c_a[0] != c_n.arg:
        print("kw args test 2 error!")
    else:
        print("kw args test 2 passed!")


def attrer():
    class Attrst:
        arg = "123"
        other = 123
        value = "asd"

        def nig(sel_f):
            return "as" + sel_f.forv()

        def forv(s_elf):
            return "sa"

        @staticmethod
        def X():
            return "sa" + Attrst().nig()

    def giga(x):
        return x.value

    if giga(ast.Constant("asd")) == giga(Attrst):
        print("attr test 1 passed!")
    else:
        print("attr test 1 error!")

    if Pidr.xxx == 123 == Attrst.other:
        print("attr test 2 passed!")
    else:
        print("attr test 2 error!")

    if Attrst.X() == "saassa":
        print("attr test 3 passed!")
    else:
        print("attr test 3 error!")


def sideff():
    from types import SimpleNamespace

    cnt = 0

    def flag(x):
        nonlocal cnt
        cnt += x
        return cnt

    def test(x=SimpleNamespace(c=1)):
        flag(x.c)
        return x

    test().c += 1
    test().c += 1

    res1 = test()
    if cnt != 6:
        print("side effect test 1 error!")
    else:
        print("side effect test 1 passed!")

    if str(res1) != "namespace(c=3)":
        print("side effect test 2 error!")
    else:
        print("side effect test 2 passed!")

    if [test(), cnt][1] != 9:
        print("side effect test 3 error!")
    else:
        print("side effect test 3 passed!")


def deltest():
    x = 10
    del x
    try:
        x
        print("del test 1 (local) error!")
    except NameError:
        print("del test 1 (local) passed!")

    class Holder:
        def __init__(self):
            self.val = 5

        def drop(self):
            del self.val

    h = Holder()
    h.drop()
    if hasattr(h, "val"):
        print("del test 2 (attr) error!")
    else:
        print("del test 2 (attr) passed!")

    p = q = 1
    del p, q
    try:
        q
        print("del test 3 (tuple) error!")
    except NameError:
        print("del test 3 (tuple) passed!")


def statictest():
    class Box:
        def __init__(self):
            self.size = 0

        def grow(self):
            self.size += 1

    class Tool:
        @staticmethod
        def read(src):
            return src.size  # src - внешний объект, .size не self и не должен переименовываться

    from types import SimpleNamespace

    ns = SimpleNamespace()
    setattr(ns, "size", 123)

    b = Box()
    b.grow()
    if Tool.read(ns) == 123 and b.size == 1:
        print("staticmethod test passed!")
    else:
        print("staticmethod test error!")


def kwclstest():
    class A:
        def run(self, val=1):
            return ("A", val)

    class B:
        def run(self, val=2):  # то же имя метода и тот же kwarg, что у A
            return ("B", val)

    if A().run(val=10) == ("A", 10) and B().run(val=20) == ("B", 20):
        print("kw cls test 1 (method collision) passed!")
    else:
        print("kw cls test 1 (method collision) error!")

    class Cfg:
        def __init__(self, factor=2, label="x"):
            self.factor = factor
            self.label = label

    c = Cfg(factor=5, label="y")
    if c.factor == 5 and c.label == "y":
        print("kw cls test 2 (ctor kwargs) passed!")
    else:
        print("kw cls test 2 (ctor kwargs) error!")

    class BaseC:
        def __init__(self, items):
            self.items = items

    class SubC(BaseC):
        pass

    if SubC(items=[1, 2, 3]).items == [1, 2, 3]:
        print("kw cls test 3 (inherited ctor) passed!")
    else:
        print("kw cls test 3 (inherited ctor) error!")


def instvartest():
    class Point:
        def __init__(self, px, py):
            self.px = px
            self.py = py

        def norm(self):
            return self.px + self.py

    pt = Point(px=3, py=4)
    if pt.px == 3 and pt.py == 4 and pt.norm() == 7:
        print("inst var test 1 (var access) passed!")
    else:
        print("inst var test 1 (var access) error!")

    from types import SimpleNamespace

    class Wrap:
        def __init__(self, w):
            self.w = w

    wr = Wrap(w=1)
    r1 = wr.w
    wr = SimpleNamespace(w="ext")
    r2 = wr.w
    if r1 == 1 and r2 == "ext":
        print("inst var test 2 (name reuse) passed!")
    else:
        print("inst var test 2 (name reuse) error!")

if __name__ == "__main__":
  closu()
  cefefe()
  kwtest()
  attrer()
  sideff()

  # new
  deltest()
  statictest()
  kwclstest()
  instvartest()
