---
layout: post
title: "Another reason to use python 3.7"
tags: python
summary: Or the discovery of dataclasses
date: 2019-05-15 21:00:00
---

Python is amazing, python 3 even more amazing and any new version brings its batch of amazing novelties! And python 3.7 doesn't break the rule. It is the first release implementing [`dataclasses` ](https://docs.python.org/3/library/dataclasses.html). This article is a short review of the new possiblities offered by this module.

Here is a example code:

    class MyClassA():
	    def __init__(self, param_a, param_b, param_c=0):
		    self.param_a = param_a
			self.param_b = param_b
			self.param_c = param_c
			
	    def __repr__(self):
		    return "param_a=%s, param_b=%s, param_c=%s" % (
			    self.param_a, 
				self.param_b, 
				self.param_c
			)
			
Do you have to write this type of code a lot of time? Then the following will be REALLY intesting for you!

Indeed, `dataclasses` is THE tool to avoid repeating code in the `__init__`, `__repr__` and a couple more methods. The equivalent of the above code using `dataclasses` is:

    from dataclasses import dataclass
	
	@dataclass
	class MyClassA():
	   param_a: int
	   param_b: int
	   param_c: int = 0 # set a default value
	   
	   
	if __name__ == '__main__':
	    mc = MyClassA(1, param_b=2)
		print(mc)

And that's all! The `dataclass` decorator will automatically generate the `__init__` and `__repr__` methods that we had to write manually above.

You have noticed the annotations style introduced in python 3.4 to make clear to the user what are the expected type of the parameters. In case you do not want to specify them, you can use `typings.Any` parameters, ie:

	import typing
    from dataclasses import dataclass
	
	@dataclass
	class MyClassA():
	   param_a: int
	   param_b: int
	   param_c: int = 0 # set a default value
	   param_d: typing.Any = None


Pretty cool? But what if I want to initialize other parameters that should not be modified through a init parameter? Easy, `dataclasses` automatically generated `__init__` method call a `__post_init__` method where you can exactly do this. For instance:

    from dataclasses import dataclass
	
    @dataclass
	class MyClassA():
	    param_a: int
	    param_b: int
	    param_c: int = 0 # set a default value

        def __post_init_(self):
	       self.initial_sum = self.param_a + self.param_b


    if __name__ == '__main__':
        mc = MyClassA(1, param_b=2, param_c=10)
	    print(mc.initial_sum)


Apart from the obvious gain in time, `dataclasses` also come with some helpful methods like:

    from dataclasses import fields
	
    fields(mc)
		
	
or:

    from dataclasses import asdict
	
    asdict(mc)
	
	# {'param_a': 1, 'param_b': 2, 'param_c': 10}


Sooo, convinced?
