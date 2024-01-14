#List and Tuples
users = ['Dave', 'John', 'Sara']
data = ['Dave', 42, True]
emptylist = []
print('Dave' in emptylist)
print(users[0])
print(users[-2])
#users.extend
#print(users)
users.insert(0, 'Bob')
print(users)

users[2:2]=['Eddie','Alex']
print(users)

users[1:3] = ['Robert','Achie']
print(users)

users.remove('Bob')
print(users)

print(users.pop())
print(users)

# del users[0]
# print(users)

users[1:2] = ['dave']
users.sort()
print(users)

users.sort(key=str.lower)
print(users)

nums = [4, 42, 78, 5]
nums.reverse()
print(nums)

# nums.sort(reverse=True)
# print(nums)

print(sorted(nums, reverse=True))
print(nums)

numscopy=nums.copy()
mynums = list(nums)
mycopy = nums[:]
print(numscopy)
print(mynums)
mycopy.sort()
print(mycopy)
print(nums)

print(type(nums))

#Tuples

mytuple= tuple(['Dave', 42, True])

anothertuple = (1,4,2,8)

print(mytuple)
print(type(mytuple))
print(type(anothertuple))


newlist = list(mytuple)
newlist.append('Neil')
newtuple = tuple(newlist)
print(newtuple)

(one, *two, hey ) = anothertuple
print(one)
print(two)
print(hey)





