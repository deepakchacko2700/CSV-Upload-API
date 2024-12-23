from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer
import csv, json


class UploadCSV(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        """
        Accept csv file and create user instances from reading the data  in the file
        """

        csv_file = request.FILES['file']

        # accept only csv file else return error
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File should be in CSV format'}, status=status.HTTP_400_BAD_REQUEST)
       
       # initialize counts to store the count of saved and rejected users and error list to store errors
        saved_records_count = 0
        rejected_records_count = 0
        error = []

        try:
            file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(file)
            header_row = next(reader) # skip the header

            for row in reader:
                # check the row contain 3 items else reject the row
                if len(row) < 3: 
                    error.append(f'Incomplete row: {row}: One of the fields name, age, email is missing')
                    rejected_records_count += 1
                    continue

                name, email, age = row
                user_dict = {'name': name, 'email': email, 'age': int(age)}
                
                # validate the input row using UserSerializer
                try:
                    serializer = UserSerializer(data=user_dict)
                    if serializer.is_valid():
                        serializer.save()
                        saved_records_count += 1
                    else:
                        error.append(f'Error in row: {row}: {serializer.errors}') # add the validation error to error list
                        rejected_records_count += 1
                except Exception as e:
                    print(f'Error: {str(e)}')
                    error.append(f'Error in row: {row}: {str(e)}')
                    rejected_records_count += 1
            response = {
                'saved_records_count': saved_records_count,
                'rejected_records_count': rejected_records_count,
                'errors': error
            }
            
            # write the response to json file
            with open('output.json', 'w') as json_file:
                json.dump(response, json_file, indent=4)

            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f'Error in processig csv file: {str(e)}')
            return Response({f'Error in processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    