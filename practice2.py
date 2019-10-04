class Animal:
    def speak(self):
        print("animal speaking")

class Dog(Animal):
    def bark(self):
        print("dog barking");
class Puppy(Dog):
    def eat(self):
        print("eating bread");
b=Puppy()
b.eat()
b.bark()
b.speak()
print(issubclass(Puppy,Animal))
