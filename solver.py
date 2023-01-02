import pandas as pd
import numpy as np
import random
import os
import json
import codecs


class COMSOAL:
    def __init__(self, data_path: str, C: int):
        self.original_data = self.__read_data(filepath=data_path)
        self.data = self.original_data.copy()
        self.C = C
        if os.path.exists('data/runtime-log.txt'):
            os.remove('data/runtime-log.txt')

    def solve(self):
        iteration_counter = 1
        number_of_stations = 1
        station_time_remaining = self.C
        assignments = {}
        unassigned = list(self.original_data['is_elemani'])
        self.__logger(f"Unassigned items: {unassigned}")

        while(unassigned != []):
            self.__logger("-----------")
            self.__logger(f"Iteration {iteration_counter}")
            selected_times = 0

            try:
                assignments[number_of_stations] == -666
            except KeyError:
                assignments[number_of_stations] = []

            alist = self.__create_alist()
            blist = self.__create_blist(alist=alist)
            flist = []

            self.__logger(f"BList: {blist}")

            # print(self.data)

            temp_dict = dict(
                zip(self.data['is_elemani'], self.data['is_suresi']))

            for item in temp_dict:
                if item in blist:

                    self.__logger(f"Station time: {station_time_remaining}")
                    self.__logger(f"Item time: {temp_dict[item]}")
                    self.__logger(
                        f"ITEM TIME: {temp_dict[item]}  STATION TIME LEFT: {station_time_remaining}")

                    item_time = temp_dict[item]

                    if item_time <= station_time_remaining:
                        flist.append(item)

            self.__logger(f"Flist: {flist}")

            # pick random number
            if len(flist) > 1:
                random_number = random.uniform(0, 1)
                random_intervals = np.linspace(0, 1, len(flist)+1)

                # search for intervals
                selected_index = -1

                for point in random_intervals:
                    if random_number >= point:
                        selected_index += 1

                selected = flist[selected_index]

                self.__logger(f"Selected: {selected}" )

                time_of_selected = (self.data[self.data['is_elemani']
                                              == selected]['is_suresi'].tolist()[0])

                self.__logger(f"Time of selected: {time_of_selected}")

                if type(station_time_remaining) == int:
                    station_time_remaining -= time_of_selected
                else:
                    station_time_remaining[0] -= time_of_selected

                assignments[number_of_stations].append(flist[selected_index])

                iteration_counter += 1

                self.__logger(f"Assignments: {assignments}")
                self.__logger(f"Station time left: {station_time_remaining}")

                # remove selected from data and oncul
                self.data = self.data[self.data['is_elemani'] != selected]
                unassigned.remove(selected)

                for row in self.data['onculler']:
                    if selected in row:
                        row.remove(selected)
                # print(unassigned)

            elif len(flist) == 1:
                selected = flist[0]
                self.__logger(f"Selected: {selected}")

                # print(f"Selected: {selected}")
                time_of_selected = (self.data[self.data['is_elemani']
                                              == selected]['is_suresi'].tolist()[0])

                self.__logger(f"Time of selected: {time_of_selected}")

                if type(station_time_remaining) == int:
                    station_time_remaining -= time_of_selected
                else:
                    station_time_remaining[0] -= time_of_selected

                assignments[number_of_stations].append(flist[0])

                self.__logger(f"Assignments: {assignments}")
                self.__logger(f"Station time left: {station_time_remaining}")

                iteration_counter += 1
                # print(station_time)
                # print(assignments)

                # remove selected from data and oncul
                self.data = self.data[self.data['is_elemani'] != selected]
                unassigned.remove(selected)

                self.data['onculler'] = self.data['onculler'].apply(lambda x: [str(i) for i in x if str(i) != str(selected)])
                self.__logger(self.data)
                # print(unassigned)

            elif flist == []:
                # flist is empty
                # open new station
                # print("*******************NEW STATION OPENED****************")
                number_of_stations += 1
                station_time_remaining = self.C


        # serialize json
        assignments_json = json.dumps(assignments, indent=4)
        # write to file
        with open('data/assignments.json', 'w') as outfile:
            outfile.write(assignments_json)

        return assignments

    def __read_data(self, filepath: str):
        data = pd.read_excel(filepath)

        data['is_elemani'] = data['is_elemani'].apply(str)
        data['is_suresi'] = data['is_suresi'].astype(int)

        data['onculler'] = data['onculler'].apply(
            lambda x: [] if pd.isnull(x) else x)
        
        data['onculler'] = data['onculler'].apply(lambda x: [x] if isinstance(x, int) else x)
        
        
        data['onculler'] = data['onculler'].apply(
            lambda x: [i.strip() for i in x.split(',')] if type(x) == str else x)

        return data

    def __create_alist(self):
        alist = {}
        length_dict = self.data.apply(lambda row: (
            row['is_elemani'], len(row['onculler'])), axis=1).to_dict()
        alist = {v[0]: v[1] for v in length_dict.values()}

        return alist

    def __create_blist(self, alist):
        blist = []
        for k, v in alist.items():
            self.__logger(f"k: {k}, v: {v}")
            if v == 0:
                blist.append(k)

        return blist
    
    def __logger(self, log):
        with codecs.open('data/runtime-log.txt', 'a+', 'utf-8') as f:
            f.write(f"{log}\n")

    def evaluate(self, assignments: dict):
        istasyon_dolu_sureler = {}
        istasyon_bos_sureler = {}

        for key, value in assignments.items():
            istasyon_dolu_sureler[key] = 0

        for key, value in assignments.items():
            for eleman in value:
                condition = self.original_data['is_elemani'] == eleman
                istasyon_dolu_sureler[key] += self.original_data[condition]['is_suresi'].values[0]
                istasyon_bos_sureler[key] = self.C  - istasyon_dolu_sureler[key]
        

        # denge gecikmesi
        # j. istasyonun denge gecikmesi
        istasyon_denge_gecikmesi = (100 * sum(istasyon_bos_sureler.values())) / (len(assignments.keys()) * self.C)
        
        # hat etkinliği
        hat_etkinligi = sum(istasyon_dolu_sureler.values()) / (self.C * len(assignments.keys()))

        # düzgünlük indeksi
        tjmax = max(istasyon_dolu_sureler.values())
        temp_sum = 0
        
        for tj in istasyon_dolu_sureler.values():
            temp_sum += ((tjmax - tj) ** 2)

        duzgunluk_indeksi = np.sqrt(temp_sum)

        result = f"İstasyon Denge Gecikmesi: {istasyon_denge_gecikmesi} %\nHat Etkinliği: {hat_etkinligi * 100} %\nDüzgünlük İndeksi: {duzgunluk_indeksi}"

        print(result)

        with codecs.open('data/evaluation-log.txt', 'w+', 'utf-8') as eval_log:
            eval_log.write(result)
