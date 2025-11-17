''' Get user's height and weight'''
height = input('Please enter your height (cm): ')
weight = input('Please enter your weight (kg): ')

h = float(height)
w = float(weight)

''' Calculate BMI '''
bmi = w / (h/100)**2
bmi = round(bmi, 1)

''' Status '''
status = 'Unknown'
if bmi<18.5:
    status = 'Underweight'
elif bmi<=25:
    status = 'Normal'
elif bmi<=30:
    status = 'Overweight'
else:
    status = 'Obese'

''' Report '''
print(bmi)
print(status)
print('Finished')