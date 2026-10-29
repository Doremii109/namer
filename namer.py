'''
Author: Doremi109
Github: https://github.com/Doremii109
Project Github: https://github.com/Doremii109/namer
'''

import ast, sys
from types import CodeType
from typing import Any, Dict, Set, List

unp = ast._Unparser if sys.version_info.minor <= 13 else __import__('_ast_unparse').Unparser

def _consts_review(c, x, y):
  nc = []
  for const in c:
    if isinstance(const, CodeType):
      try:
        idx = (_const:=const.co_consts).index(x)
        (_const:=list(_const))[idx] = y
      except ValueError:_const = list(const.co_consts)
      nc.append(const.replace(co_consts=tuple(_const)))
    else: nc.append(const)
  return nc

def _del_space(obj: str, remap: list[tuple[str]]):
  _consts = list((_obj:=getattr(unp, obj)).__code__.co_consts)
  for x, y in remap:
    try:_consts[_obj.__code__.co_consts.index(x)] = y
    except ValueError:_consts = _consts_review(_consts, x, y)
  _obj.__code__ = _obj.__code__.replace(co_consts=tuple(_consts))

unp.cmpops = {
  "Eq": "==",
  "NotEq": "!=",
  "Lt": "<",
  "LtE": "<=",
  "Gt": ">",
  "GtE": ">=",
  "Is": " is ",
  "IsNot": " is not ",
  "In": " in ",
  "NotIn": " not in ",
}

def del_space():
  _del_space('visit_arguments', [(", /", ",/")])
  for obj in ['visit_AnnAssign', 'visit_MatchMapping', 'visit_Lambda', 'visit_Dict', 
              'visit_DictComp', 'visit_arg', 'visit_arguments']:
    _del_space(obj, [(": ", ":")])
  for obj in ['visit_ClassDef', '_type_params_helper', 'items_view', 'visit_FunctionType', 
              'visit_Import', 'visit_ImportFrom', 'visit_Assert', 'visit_Global', 
              'visit_Nonlocal', 'visit_With', 'visit_AsyncWith', 'visit_List', 
              'visit_Set', 'visit_MatchSequence', 'visit_MatchClass', 'visit_Delete', 
              'visit_Call', 'visit_MatchMapping', 'visit_Dict', 'visit_arguments']:
    _del_space(obj, [(", ", ",")])
  _del_space('_function_helper', [(" -> ", "->")])
  _del_space('visit_FunctionType', [(" -> ", "->")])
  _del_space('visit_MatchOr', [(" | ", "|")])
  _del_space('visit_BinOp', [(" ", "")])
  _del_space('visit_AugAssign', [(" ", ""), ("= ", "=")])
  _del_space('visit_Compare', [(" ", "")])
  _del_space('fill', [("    ", " ")])
  _del_space('visit_Assign', [(" = ", "=")])
  _del_space('visit_AnnAssign', [(" = ", "=")])
  _del_space('visit_TypeAlias', [(" = ", "=")])
  _del_space('visit_NamedExpr', [(" := ", ":=")])

del_space()

pref, np = '_0x', 0
def genName() -> str:
	global np
	return f'{pref}{abs(hash(str(np:=np + 1)))}'
	# return f'{pref}{(np:=np + 1)}'

def astP(c: str) -> list[ast.AST]:
  return ast.parse(c).body

cl_attr, pr_var, pr_attr, all_names, slf_n, built_n, args_mp, arg_names, cls_obf = set(), set(), set(), {}, {}, {}, {}, {}, set()

class BuiltR(ast.NodeTransformer):
	def __init__(self, pr_var_bn: Set[str], built: Dict[str, Any] = __builtins__):
		self.pr_var_bn: Set[str] = pr_var_bn
		self.built_dir: Dict[str, Any] = dir(built)
	def visit_Name(self, node):
		if isinstance(node.ctx, ast.Load) and (n:=node.id) in self.built_dir and n not in self.pr_var_bn and n != 'super':
			node.id = built_n.setdefault(n, genName())
		return node

def _is_magic_name(n: str):
	return not((n.startswith('__') and n.endswith('__')) or
			   n.startswith('visit_') # for ast
			   )

def _is_static(fn: ast.FunctionDef | ast.AsyncFunctionDef):
	return any(getattr(d, 'id', getattr(d, 'attr', None)) == 'staticmethod' for d in fn.decorator_list)

def _target_names(t):
	if isinstance(t, ast.Name): return {t.id}
	if isinstance(t, ast.Starred): return _target_names(t.value)
	if isinstance(t, (ast.Tuple, ast.List)):
		s = set()
		for e in t.elts: s |= _target_names(e)
		return s
	return set()

class PreScan(ast.NodeVisitor):
	def __init__(self, track_instances: bool = False):
		self.c_stack: List[str] = []
		self.local_defs: Set[str] = None
		self.track_instances: bool = track_instances
		self.inst_vars: Set[str] = set()
	def visit(self, node):
		if self.local_defs is None:
			self.local_defs = {n.name for n in ast.walk(node) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
			if self.track_instances:
				self._collect_inst_vars(node)
		return super().visit(node)
	def _collect_inst_vars(self, tree):
		local_cls = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
		is_ctor = lambda v: isinstance(v, ast.Call) and getattr(v.func, 'id', None) in local_cls
		ctor, other = set(), set()
		for nd in ast.walk(tree):
			if isinstance(nd, ast.Assign):
				for t in nd.targets: (ctor if is_ctor(nd.value) else other).update(_target_names(t))
			elif isinstance(nd, ast.AnnAssign):
				ok = (isinstance(nd.annotation, ast.Name) and nd.annotation.id in local_cls) or is_ctor(nd.value)
				(ctor if ok else other).update(_target_names(nd.target))
			elif isinstance(nd, (ast.AugAssign, ast.For, ast.AsyncFor)):
				other.update(_target_names(nd.target))
			elif isinstance(nd, ast.comprehension):
				other.update(_target_names(nd.target))
			elif isinstance(nd, ast.NamedExpr):
				other.update(_target_names(nd.target))
			elif isinstance(nd, ast.withitem) and nd.optional_vars:
				other.update(_target_names(nd.optional_vars))
			elif isinstance(nd, ast.ExceptHandler) and nd.name:
				other.add(nd.name)
			elif isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
				a = nd.args
				for ar in a.posonlyargs + a.args + a.kwonlyargs + ([a.vararg] if a.vararg else []) + ([a.kwarg] if a.kwarg else []):
					other.add(ar.arg)
		self.inst_vars = ctor - other
	def visit_Call(self, node):
		self.generic_visit(node)
		if getattr(node.func, 'id', getattr(node.func, 'attr', None)) not in self.local_defs:
			for kw in node.keywords:
				if kw.arg:
					pr_attr.add(kw.arg)
	def visit_Attribute(self, node):
		self.generic_visit(node)
		is_self = isinstance(node.value, ast.Name) and any(node.value.id in sn for sn in slf_n.values())
		is_cls = isinstance(node.value, ast.Name) and node.value.id in slf_n
		is_cls_inst = isinstance(node.value, ast.Call) and getattr(node.value.func, 'id', '') in slf_n
		is_inst = isinstance(node.value, ast.Name) and node.value.id in self.inst_vars
		if not(is_self or is_cls or is_cls_inst or is_inst):
			pr_attr.add(node.attr)
	def visit_ClassDef(self, node):
		sn: Set[str] = slf_n.setdefault(node.name, set())
		self.c_stack.append(node.name)
		for n in ast.walk(node):
			if isinstance(n, ast.NamedExpr) and isinstance(trg:=n.target, ast.Name) and isinstance(trg.ctx, ast.Store):
				cl_attr.add(trg.id)
		for i in node.body:
			if isinstance(i, (ast.FunctionDef, ast.AsyncFunctionDef)) and i.args.args and not _is_static(i):
				sn.add(i.args.args[0].arg)
		for i in node.body:
			if isinstance(i, ast.Assign):
				cl_attr.update(t.id for t in i.targets if isinstance(t, ast.Name))
			elif isinstance(i, (ast.AnnAssign, ast.NamedExpr)) and isinstance(i.target, ast.Name):
				cl_attr.add(i.target.id)
			elif isinstance(i, (ast.FunctionDef, ast.AsyncFunctionDef)):
				cl_attr.add(i.name)
				if i.args.args and not _is_static(i):
					s_n = i.args.args[0].arg
					for n in ast.walk(i):
						if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store) and getattr(n.value, 'id', '') == s_n:
							cl_attr.add(n.attr)
			elif isinstance(i, ast.ClassDef):
				cl_attr.add(i.name)
		self.generic_visit(node)
		self.c_stack.pop()

class CollectNames(ast.NodeTransformer):
	def __init__(self):
		self.scopes: List[Dict[str, str]] = [all_names]
		self.scope_flags = [set()]
		self.in_class_body = [False]
	def visit_ClassDef(self, node):
		is_nested = self.in_class_body[-1]
		if ((n:=node.name) not in pr_var and _is_magic_name(n))and not(is_nested and n in pr_attr):
			if is_nested and n in cl_attr: node.name = all_names.setdefault(n, genName())
			else: node.name = self.scopes[-1].setdefault(n, genName())
		cls_obf.add(node.name) # для kwargs в класса/__init__
		self.in_class_body.append(True)
		self.scope_flags.append(set())
		self.generic_visit(node)
		self.scope_flags.pop()
		self.in_class_body.pop()
		return node
	def visit_FunctionDef(self, node):
		is_method = self.in_class_body[-1]
		if not((n:=node.name) in pr_var or (is_method and n in pr_attr)) and _is_magic_name(n):
			if is_method and n in cl_attr: node.name = all_names.setdefault(n, genName())
			else: node.name = self.scopes[-1].setdefault(n, genName())
		for _d in node.args.defaults: self.visit(_d)
		for _d in node.args.kw_defaults:
			if _d is not None: self.visit(_d)
		_saved_def, _saved_kw = node.args.defaults, node.args.kw_defaults
		node.args.defaults, node.args.kw_defaults = [], [None] * len(_saved_kw)
		self.in_class_body.append(False)
		orig_args = {a.arg for a in node.args.args + getattr(node.args, 'kwonlyargs', []) + getattr(node.args, 'posonlyargs', [])}
		self.scopes.append({})
		self.scope_flags.append(set())
		self.generic_visit(node)
		node._scope = self.scopes.pop()
		args_mp.setdefault(node.name, {}).update({k: v for k, v in node._scope.items() if k in orig_args})
		self.scope_flags.pop()
		self.in_class_body.pop()
		node.args.defaults, node.args.kw_defaults = _saved_def, _saved_kw
		return node
	visit_AsyncFunctionDef = visit_FunctionDef
	def visit_Global(self, node):
		self.scope_flags[-1].update(node.names)
		return node
	visit_Nonlocal = visit_Global
	def store_name(self, n):
		if n in self.scope_flags[-1]:
			for scope in reversed(self.scopes[:-1]):
				if n in scope:
					return scope[n]
			return all_names.setdefault(n, genName())
		return self.scopes[-1].setdefault(n, genName())
	def visit_Name(self, node):
		if isinstance(node.ctx, (ast.Store, ast.Del)) and (n:=node.id) and _is_magic_name(n):
			if self.in_class_body[-1] and n in cl_attr and n in pr_attr:
				print('[ERROR] class attr/name using out class, skipping:', n)
			elif n not in pr_var:
				if self.in_class_body[-1] and n in cl_attr:
					node.id = all_names.setdefault(n, genName())
				else:
					node.id = self.store_name(n)
		return node
	def visit_arg(self, node):
		self.generic_visit(node)
		if (n:=node.arg) not in pr_var:
			node.arg = self.scopes[-1][n] = arg_names.setdefault(n, genName())
		return node
	def visit_Attribute(self, node):
		self.generic_visit(node)
		if isinstance(node.ctx, (ast.Store, ast.Del)) and (n:=node.attr) in cl_attr and _is_magic_name(n):
			if n not in pr_attr:
				node.attr = all_names.setdefault(n, genName())
		return node
	def visit_ExceptHandler(self, node):
		self.generic_visit(node)
		if (exc:=getattr(node, 'name', None)) and exc not in pr_var:
			node.name = self.store_name(exc)
		return node
	def visit_MatchAs(self, node):
		self.generic_visit(node)
		if (n:=getattr(node, 'name', None)) and n not in pr_var and _is_magic_name(n):
			node.name = self.store_name(n)
		return node
	visit_MatchStar = visit_MatchAs
	def visit_MatchMapping(self, node):
		self.generic_visit(node)
		if (n:=getattr(node, 'rest', None)) and n not in pr_var and _is_magic_name(n):
			node.rest = self.store_name(n)
		return node

class ReplNames(ast.NodeTransformer):
	def __init__(self):
		self.scopes = [all_names]
	def resolve(self, n):
		for scope in reversed(self.scopes):
			if n in scope: return scope[n]
		return n
	def visit_FunctionDef(self, node):
		self.scopes.append(getattr(node, '_scope', {}))
		self.generic_visit(node)
		self.scopes.pop()
		return node
	visit_AsyncFunctionDef = visit_FunctionDef
	def visit_Name(self, node):
		if (isinstance(node.ctx, ast.Load) and (n:=node.id) not in pr_var) and (resolved:=self.resolve(n)) != n:
			node.id = resolved
		return node
	def visit_arg(self, node):
		self.generic_visit(node)
		if (n:=node.arg) not in pr_var:
			node.arg = self.resolve(n)
		return node
	def visit_Call(self, node):
		self.generic_visit(node)
		if (obf_n:=getattr(node.func,'id',getattr(node.func, 'attr', None))) in args_mp:
			for kw in node.keywords:
				if getattr(kw, 'arg', None) in (arg_map:=args_mp[obf_n]):
					kw.arg = arg_map[kw.arg]
		elif obf_n in cls_obf: # для kwargs в класса/__init__
			for kw in node.keywords:
        # именно из-за того что я проверяю только __init__, при track_instances
        # код может ломаться, поэтому у меня сначала ренейм, а потом уже skipInit,
        # иначе код бы уже на tester.py ломался, да и я хз как это делать, не проверяя __init__
				if getattr(kw, 'arg', None) in (arg_map:=args_mp.get('__init__', {})): 
					kw.arg = arg_map[kw.arg]
		return node
	def visit_Global(self, node):
		node.names = [self.resolve(n) if n not in pr_var else n for n in node.names]
		return node
	visit_Nonlocal = visit_Global
	def visit_Attribute(self, node):
		self.generic_visit(node)
		if isinstance(node.ctx, ast.Load) and (n:=node.attr) in cl_attr and n not in pr_attr and (resolved:=all_names.get(n, n)) != n:
			node.attr = resolved
		return node
	def visit_MatchAs(self, node):
		self.generic_visit(node)
		if (n:=getattr(node, 'name', None)) not in pr_var and (resolved:=self.resolve(n)) != n:
			node.name = resolved
		return node
	visit_MatchStar = visit_MatchAs
	def visit_MatchMapping(self, node):
		self.generic_visit(node)
		if (n:=getattr(node, 'rest', None))not in pr_var and (resolved:=self.resolve(n)) != n:
			node.rest = resolved
		return node
	def visit_MatchClass(self, node):
		self.generic_visit(node)
		node.kwd_attrs = [all_names.get(attr, attr) if attr in cl_attr and attr not in pr_attr else attr for attr in node.kwd_attrs]
		return node


class skipInit(ast.NodeTransformer): # штука для 'скрытия' __init__
  def visit_ClassDef(self, node):
    is_mc = any((kw.arg=='metaclass') for kw in node.keywords)
    for i,f in enumerate(node.body):
      if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)) and f.name == '__init__':
        ind = i
        f.name = (nfn:=genName());break
    else:return node

    if is_mc:
      obj = astP(f'locals().update({{"__init__":{nfn} }})')[0]
      node.body.insert(ind+1, obj)
    else:
      s = astP(f'''
class {(mc:=genName())}(type):
  def __call__({(smc:=genName())}, *{(args:=genName())}, **{(kwargs:=genName())}):
    {smc}.{nfn}(({(obj:=genName())}:={smc}.__new__({smc})), *{args}, **{kwargs})
    return {obj}
''')
      node.keywords.append(ast.keyword('metaclass', astP(mc)[0].value))
      node = s + [node]
      
    return node


def rename(
  code: str | ast.AST, 
  
  # тут кароче указываешь либо нихуя, либо __builtins__
  # вообще это нужно, если ты юзаешь namer в импортах или если надо, чтобы builtins тоже переименовывались
	built: bool | Dict[str, Any] = False, 
 
  # ремапить атрибуты через переменную var=какой_то_класс(...)
	# осторожно: может ломать обфусцированные код, хотя это редко
	track_instances: bool = False
	) -> str:
	_is_ast = isinstance(code, ast.Module)
	PreScan(track_instances).visit(tr:=(code if _is_ast else ast.parse(code)))
	pr_var_bn = pr_var.copy()
	for _tr in (CollectNames(),ReplNames(),skipInit()):
		tr = _tr.visit(tr)

	_h = ''
	if built:
		tr: ast.Module = BuiltR(pr_var_bn, built).visit(tr)
		_h = f'{",".join(built_n.values())} = {",".join(built_n.keys())}\n'
	if _is_ast: 
		_h = astP(_h)
		tr.body.insert(0, _h)

	return (tr if _is_ast else _h+ast.unparse(tr))

if __name__ == '__main__':
	# cho_kavo_gaga_gigi = open('./cyron/VM.py', 'r', encoding='utf8', errors='ignore').read()
	file = 'tester.py'
	cho_kavo_gaga_gigi = open(file, 'r', encoding='utf8', errors='ignore').read()
	open(file[:-3]+'_dor_rename.py', 'w', encoding='utf8').write(rename(cho_kavo_gaga_gigi, track_instances=True))
