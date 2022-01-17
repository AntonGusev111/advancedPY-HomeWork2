import csv
import re


class phone_book ():

  def __init__(self,file_name):
    self.file_name=file_name
    self.contats_list = self.read()
    self.result_list = self.pars()
    self.format_lists = self.format_lists()
    self.phonebook_result = self.unick_lists()

  def read(self):
    with open(self.file_name) as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)
      return contacts_list

  def pars (self):
    Phone_pattern = r"(\+7|8)(\s*|)(\(|)(\d\d\d)(\)|)(\-|\s|)(\d\d\d)(\-|)(\d\d)(\-|)(\d+)(\s|)(\(|)([а-яА-я.]+|)(\s|)(\s|)(\d+|)(\)|)"
    result_list = []
    for value in self.contats_list:
      value[5] = re.sub(Phone_pattern, r"+7(\4)\7-\9-\11 \14\17", value[5])
      result_list.append(value)
    return result_list

  def format_lists(self):
    dict_list = []
    final_dict = {"lastname":'',"firstname":'','surname':'','organization':'','position':'','phone':'','email':''}
    for i in self.result_list:
      if len(i[1].split()) >= 2:
        final_dict['firstname'] = i[1].split()[0]
        final_dict['surname'] = i[1].split()[1]
        final_dict['lastname'] = i[0]
      elif len(i[0].split()) == 1:
        final_dict['lastname'] = i[0]
        final_dict['firstname'] = i[1]
        final_dict['surname'] = i[2]
      elif len(i[0].split()) >= 2:
        final_dict['lastname'] = i[0].split()[0]
        final_dict['firstname'] = i[0].split()[1]
        try:
          final_dict['surname'] = i[0].split()[2]
        except:
          final_dict['surname'] = i[1]
      final_dict['organization'] = i[3]
      final_dict['position'] = i[4]
      final_dict['phone'] = i[5]
      final_dict['email'] = i[6]
      dict_list.append(list(final_dict.values()))
      final_dict = {"lastname": '', "firstname": '', 'surname': '', 'organization': '', 'position': '', 'phone': '','email': ''}
    return dict_list

  def unick_lists(self):
    final_list = self.format_lists
    N = len(self.format_lists)+1
    del_index= []
    for i in range(N-1):
      for search in range (i+1,N-1):
        if final_list[i][0] == final_list[search][0] and final_list[i][1] == final_list[search][1]:
          for value in range (7):
            if final_list[i][value] == '':
              final_list[i][value] = final_list[search][value]
          del_index.append(search)

    for i in reversed(del_index):
     del final_list[i]
    return final_list

  def write(self):
    with open("phonebook_result.csv", "w",newline='') as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(self.phonebook_result)


file_name = "phonebook_raw.csv"
phone = phone_book(file_name)
phone.write()

