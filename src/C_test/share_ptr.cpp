#include <iostream>
// #include <memory>
using namespace std;

template<typename T>
class SharedPtr{
    using Deleter = void (*)(T*);
    T* p = nullptr;
    size_t* pctr = nullptr;
    Deleter del = nullptr;

    void swap(SharedPtr& SharedPtr){
        using std::swap;
        swap(this->p, SharedPtr.p);
        swap(this->pctr, SharedPtr.pctr);
        swap(this->del, SharedPtr.del);
    }

public:
SharedPtr(T* p = nullptr, Deleter del = nullptr):
    p(p), pctr(new size_t(p != nullptr)), del(del){}
SharedPtr(const SharedPtr& SharedPtr) : p(SharedPtr.p), pctr(SharedPtr.pctr),
    del(SharedPtr.del){
        ++*(this->pctr);
    }
SharedPtr(SharedPtr&& sharedPtr): SharedPtr(){
    this->swap(sharedPtr);
}
SharedPtr& operator=(SharedPtr sharedPtr){
    this->swap(sharedPtr);
    return *this;
}
~SharedPtr(){
    if(this->p == nullptr){
        return;
    }
    if(--*(this->pctr) == 0){
        this->del ? this->del(this->p) : delete this->p;
        delete pctr;
    }
}
void reset(T *p = nullptr, Deleter del = nullptr){
    SharedPtr wrapper(p, del);
    this->swap(wrapper);
}
T& operator*() {return *p;}
T* operator->() {return p;}
};
class Foo{
public:
    int n;
    Foo(int n): n(n){}
    ~Foo(){cout<<n<<" Foo deleted"<<endl;}
};

int main(int argc, char** argv){
    SharedPtr<Foo> f1(new Foo(10));
    SharedPtr<Foo> f2(new Foo(20));
    SharedPtr<Foo> f3(f1);

    f2 = f1;
    f3 = SharedPtr<Foo>(new Foo(30));
    SharedPtr<int> arr(new int[3]{1, 2, 3}, [](int *arr){delete [] arr;});
    
    return 0;
}