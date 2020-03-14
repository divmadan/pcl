class Shape {
public:
  Shape() {
  }
  ~Shape() {
  };
  virtual double area() = 0;
};

class Square : public Shape {
private:
  double width;
public:
  Square(double w) : width(w) { };
  double area();
};