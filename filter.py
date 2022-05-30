def filter(filterPlace, filterStartdate, filterEnddate, filterClass, filterMaxPrice):
    if filterPlace != "":
                    cur.execute("SELECT UserID FROM User INNER JOIN Adresse ON Adresse.AdressID = User.Adresse WHERE Adresse.Ort == (?)", [(filterPlace)]).fetchall() 
                    if filterStartdate != "":
        if filterStartdate != "":
            if filterEnddate != "":
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                        return "SELECT UserID FROM User INNER JOIN Adresse ON Adresse.AdressID = user.Adresse WHERE Adresse"
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
            else:
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
        else:
            if filterEnddate != "":
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
            else:
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
    else:
        if filterStartdate != "":
            if filterEnddate != "":
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
            else:
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
        else:
            if filterEnddate != "":
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
            else:
                if filterClass != "":
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")
                else:
                    if filterMaxPrice != "":
                        print("end")
                    else:
                        print("end")