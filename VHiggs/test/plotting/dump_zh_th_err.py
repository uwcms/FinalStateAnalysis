import theory_errors

for i in [110, 120, 130, 140, 150, 160]:
    print 'mass:', i, 'pdf:', theory_errors.get_pdf_err_str(i, 4), \
            'scale:', theory_errors.get_scale_err_str(i, 4)
