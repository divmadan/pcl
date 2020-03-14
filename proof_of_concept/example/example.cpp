#include "example.h"
#include<iostream>

double 
Square::area()
{
    return Square::width*Square::width;
}

int
main (int argc, char** argv)
{
    Square s(10.0);
    std::cout<<"Square area: "<<s.area();
    return(0);
}