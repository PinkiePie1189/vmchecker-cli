import requests
import argparse
from getpass import getpass


HOST_URL = 'https://vmchecker.cs.pub.ro'
ALL_GRADES_URL = '/services/services.py/getAllGrades'
SUBMIT_URL = '/services/services.py/uploadAssignment'


def login():
    while (True):
        print('Please login with your cs.curs.ro credidentials')
        username = input("Username: ")
        password = getpass()
        r = requests.post('https://vmchecker.cs.pub.ro/services/services.py/login', data = {'username' : username, 'password' : password}, verify = False)
        if (r.json()['info'] == 'Succesfully logged in'):
            return r.cookies
        else:
            print("Invalid credidentials, please try again")


def searchStudent(studentId, courseId, loginCookies):
    r = requests.get('{}?courseId={}'.format(HOST_URL + ALL_GRADES_URL, courseId), cookies = loginCookies, verify = False)
    allGrades = eval(r.text)
    foundStudent = False
    for student in allGrades:
        if (args.target == student['studentId']):
            print(student['results'])
            return True
    return False

def submitAssignment(courseId, assignId, filename, loginCookies):
    with open(filename, 'rb') as f:
        multipartRequestBody = {'archiveFile' : (filename, f.read(), 'application/zip'),
                                'courseId' : (None, courseId),
                                'assignmentId': (None, assignId)}
        r = requests.post(HOST_URL + SUBMIT_URL, cookies = loginCookies, files = multipartRequestBody, verify = False)
        pretty_print_POST(r.request)

        # TODO check for other sources of error
        if (r.status_code == 200):
            return True
    return False

if __name__ == '__main__':
    loginCookies = login()

    parser = argparse.ArgumentParser(description='VMChecker Command Line Interface')
    parser.add_argument('--target', dest='target', help='The student id on which you want to spy')
    parser.add_argument('--course', dest='course', help = 'A course id')
    parser.add_argument('--submit', dest='submit', help = 'Submit an assignment', action = 'store_true')
    parser.add_argument('--assign', dest='assignId', help = 'An assignment id')
    parser.add_argument('--filename', dest='filename', help = 'The filename for submission')
    args = parser.parse_args()


    if (args.target is not None and args.course is not None):
        if (searchStudent(args.target, args.course, loginCookies) == False):
            print("No such student!")
    elif (args.submit is not None):
        if (submitAssignment(args.course, args.assignId, args.filename, loginCookies) == False):
            print("Couldn't submit assignment")

