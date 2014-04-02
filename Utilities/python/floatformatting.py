def odm(num):
   if num < 10 and num >=1:
      return 0
   else:
      if num > 1:
         return 1+odm(num/10.)
      else:
         return -1+odm(num*10.)

def smart_float_format(num, error_mark=' #pm '):
   if isinstance(num, tuple) or isinstance(num, list):
      #number + error
      value = num[0]
      error = num[1]
      odm_e = odm(error)
      float_straight_format = ''
      if odm_e < 0:
         float_straight_format = '%.'+str(1-odm_e)+'f '
      else:
         float_straight_format = '%.0f'
      straght_print = (float_straight_format+error_mark+float_straight_format) % (value, error)
      exp_format = ('(%.1f'+error_mark+'%.1f)e%i') % ( value*10**(-odm_e), error*10**(-odm_e), odm_e)
      return min([straght_print, exp_format], key=len)
      
