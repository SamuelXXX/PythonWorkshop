# -*- encoding:utf-8 -*-
import copy
import json

ATOM_TYPE_DESCRIPTOR=[
	(int,"int"),
	(float,"float"),
	(bool,"bool"),
	(str,"std::string")
]

TYPE_ID_2_TYPE_STR={idx:items[1] for idx,items in enumerate(ATOM_TYPE_DESCRIPTOR)}
TYPE_ID_2_TYPE_OBJ={idx:items[0] for idx,items in enumerate(ATOM_TYPE_DESCRIPTOR)}
TYPE_OBJ_2_TYPE_ID={items[0]:idx for idx,items in enumerate(ATOM_TYPE_DESCRIPTOR)}

STRUCT_TEMPLATE="""
struct %(STRUCT_NAME)%
{
private:
	%(VAR_DEC)%
public:
	%(VAR_GETTER)%
}
"""

class NestedStructType(object):
	def __init__(self, type_id, struct_dict):
		self.id=type_id
		self.struct_dict=copy.deepcopy(struct_dict)
		self.signature=json.dumps(self.struct_dict)
		if "__is_list__" in struct_dict:
			self.is_list=True
			self.struct_dict.pop("__is_list__")
		else:
			self.is_list=False

	def gen_struct_body(self, struct_name_func):
		struct_body=STRUCT_TEMPLATE
		struct_body=struct_body.replace("%(STRUCT_NAME)%",struct_name_func(self.id))
		struct_body=struct_body.replace("%(VAR_DEC)%",self.gen_var_declaration(struct_name_func))
		struct_body = struct_body.replace("%(VAR_GETTER)%", self.gen_var_getter(struct_name_func))
		return struct_body

	def gen_var_declaration(self,struct_name_func):
		line_offset="\n"+"\t"

		code_body=""
		for property_name,property_type_id in self.struct_dict.items():
			var_name="_%s"%property_name
			if property_type_id in TYPE_ID_2_TYPE_STR:
				type_str=TYPE_ID_2_TYPE_STR[property_type_id]
			else:
				type_str=struct_name_func(property_type_id)

			code_body+="%s %s;"%(type_str,var_name)
			code_body+=line_offset

		return code_body

	def gen_var_getter(self,struct_name_func):
		line_offset = "\n" + "\t"

		code_body = ""
		for property_name, property_type_id in self.struct_dict.items():
			var_name = "_%s" % property_name
			if property_type_id in TYPE_ID_2_TYPE_STR:
				ret_type_str = TYPE_ID_2_TYPE_STR[property_type_id]
			else:
				ret_type_str = struct_name_func(property_type_id)+"&"

			code_body += "%s get%s() noexcept {return %s;}" % (ret_type_str, var_name, var_name)
			code_body += line_offset

		return code_body

class CppStructGenerator(object):
	def __init__(self):
		self.source_dict=None
		self.preprocessed_dict=None

		self.built_nested_struct_type=None # type signature to NestedStructDescriptor
		self.current_available_type_id=100

	def set_source(self, source_dict):
		self.source_dict=source_dict
		self.__make_preprocessed_dict()
		self.built_nested_struct_type={}
		self.current_available_type_id = 100

	# region Preprocessing
	def __make_preprocessed_dict(self):
		if self.source_dict is None:
			return

		self.preprocessed_dict=self.__recur_preprocessing(self.source_dict)

	def __recur_preprocessing(self, target_object):
		obj_type=type(target_object)

		if obj_type in TYPE_OBJ_2_TYPE_ID:
			return TYPE_OBJ_2_TYPE_ID[obj_type]
		elif obj_type in (tuple,list):
			ret_dict = {str(i):self.__recur_preprocessing(v) for i, v in enumerate(target_object)}
			ret_dict["__is_list__"]=0
			return ret_dict
		elif obj_type is dict:
			return {str(k):self.__recur_preprocessing(v) for k, v in target_object.items()}
	# endregion

	# region Compiling
	def compile(self):
		self.__recur_compile(self.preprocessed_dict)

	def __recur_compile(self,compiling_dict):
		update_items={}

		for k, v in compiling_dict.items():
			if type(v) is dict:
				update_items[k]=self.__recur_compile(v)

		compiling_dict.update(update_items)
		return self.__build_struct_type(compiling_dict)

	def __build_struct_type(self, struct_dict):
		new_struct_type=NestedStructType(self.current_available_type_id, struct_dict)
		if new_struct_type.signature in self.built_nested_struct_type:
			return self.built_nested_struct_type[new_struct_type.signature].id
		else:
			self.current_available_type_id+=1
			self.built_nested_struct_type[new_struct_type.signature]=new_struct_type
			return new_struct_type.id
	# endregion

	def get_root_type_id(self):
		return max([t.id for t in self.built_nested_struct_type.values()])

	def output(self, root_struct_name, struct_name_func=None):
		code = ""
		root_id=self.get_root_type_id()

		def wrapped_struct_name_func(type_id):
			if type_id==root_id:
				return root_struct_name
			elif struct_name_func is None:
				return "%s_NestedStruct_%s"%(root_struct_name,type_id)
			else:
				return struct_name_func(type_id)

		for struct in self.built_nested_struct_type.values():
			code += struct.gen_struct_body(wrapped_struct_name_func)
		return code

generator=CppStructGenerator()

test_dict={
	"key1":[1,2,3],
	"key2":{
		1:False,
		2:[1.0,2.0],
	},
	"key3":{
		1:False,
		2:[1.0,2.0],
	},
	"key4":{
		1:False,
		2:[1.0,2.0],
	},
	"3":[1,2,3.0],
}

generator.set_source(test_dict)
generator.compile()

with open("test.hpp","w") as fp:
	fp.write(generator.output("Test"))
