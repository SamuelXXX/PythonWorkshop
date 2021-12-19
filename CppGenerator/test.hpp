
struct Test_NestedStruct_100
{
private:
	int _0;
	int _1;
	int _2;
	
public:
	int get_0() noexcept {return _0;}
	int get_1() noexcept {return _1;}
	int get_2() noexcept {return _2;}
	
}

struct Test_NestedStruct_101
{
private:
	float _0;
	float _1;
	
public:
	float get_0() noexcept {return _0;}
	float get_1() noexcept {return _1;}
	
}

struct Test_NestedStruct_102
{
private:
	bool _1;
	Test_NestedStruct_101 _2;
	
public:
	bool get_1() noexcept {return _1;}
	Test_NestedStruct_101& get_2() noexcept {return _2;}
	
}

struct Test_NestedStruct_103
{
private:
	int _0;
	int _1;
	float _2;
	
public:
	int get_0() noexcept {return _0;}
	int get_1() noexcept {return _1;}
	float get_2() noexcept {return _2;}
	
}

struct Test
{
private:
	Test_NestedStruct_100 _key1;
	Test_NestedStruct_102 _key2;
	Test_NestedStruct_102 _key3;
	Test_NestedStruct_102 _key4;
	Test_NestedStruct_103 _3;
	
public:
	Test_NestedStruct_100& get_key1() noexcept {return _key1;}
	Test_NestedStruct_102& get_key2() noexcept {return _key2;}
	Test_NestedStruct_102& get_key3() noexcept {return _key3;}
	Test_NestedStruct_102& get_key4() noexcept {return _key4;}
	Test_NestedStruct_103& get_3() noexcept {return _3;}
	
}
