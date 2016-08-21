import webbrowser
import httplib
from datetime import datetime, tzinfo, timedelta
import urllib2
import json

# =======================================================================


class Zone(tzinfo):
    """ Used for UTC time zone conversion
    Borrowed from http://stackoverflow.com/a/4770688
    """
    def __init__(self, offset=0, isdst=True, zone_name="UTC"):
        self.offset = offset
        self.isdst = isdst
        self.name = zone_name
        self.zone_dict = {"UTC": 0, "GMT": 0, "AST": -4, "EST": -5, "CST": -6,
                 "MST": -7, "PST": -8, "CET": 1, "UTC+2": 2, "UTC+3": 3,
                 "UTC+4": 4, "UTC+5": 5, "UTC+6": 6, "UTC+7": 7, "UTC+8": 8, "UTC+9": 9,
                 "UTC+10": 10, "UTC+11": 11, "UTC+12": 12, "UTC+13": 13}

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
        return self.name


# ======================================================================


def convert_from_utc(utc_time, zone="EST"):
    """ Converts UTC time to specified time zone (ie. EST, CST, PST)
    :param utc_time: time_in_utc
    :param zone: target_time_zone_variable_assigned_using_Zone() (eg. EST, CST, PST)
    :return: time_converted_to_target_time_zone
    """
    utc = Zone(0, False, "UTC")
    if zone in Zone().zone_dict.keys():
        offset = Zone().zone_dict[zone]
        zone = Zone(offset, True, zone)
    else:
        zone = utc
    unconverted = datetime.strptime(utc_time, '%B %d, %Y %H:%M:%S UTC')
    unconverted = unconverted.replace(tzinfo=utc)
    conv_time = unconverted.astimezone(zone)
    converted = conv_time.strftime('%B %d, %Y %H:%M:%S %Z')
    return converted


def get_countdown(utc_date):
    """ Returns days, hours, minutes, and seconds until specified UTC date/time
    :param utc_date: variable_assigned_using_Zone() (eg. EST, CST, PST)
    :return: countdown_to_specified_date (format: "x days, hh:mm:ss")
    """
    try:
        f_launch_date = datetime.strptime(utc_date, "%B %d, %Y %H:%M:%S UTC")
        utc_now = datetime.utcnow()
        diff = f_launch_date - utc_now
        cd_clock = str(diff)[:-7]
    except IndexError:
        cd_clock = ""
    return cd_clock


# Launch Library information retrieval stuff ===========================

def get_launches(number_of_launches=None):
    """ Retrieves all available information for specified number of launches from launchlibrary.net
    :param number_of_launches: number_of_launches_to_retrieve_or_blank_for_all_-_string
    :return: dictionary_containing_launch_information
    """
    if number_of_launches is None:
        txt_eval = get_info("https://launchlibrary.net/1.1/launch?mode=list")
        total = txt_eval['total']
    else:
        total = number_of_launches
    launch_dict = get_info("https://launchlibrary.net/1.1/launch/next/%d?mode=verbose" % total)
    full_launch_dict = insert_additional_info(launch_dict)
    full_launch_dict_with_names = give_names_to_ids(full_launch_dict)
    return full_launch_dict_with_names


def insert_additional_info(l_dict):
    for launch_no in xrange(len(l_dict['launches'])):
        # Get missions details if they exist
        if len(l_dict['launches'][launch_no]['missions']) > 0:
            for mission_no in xrange(len(l_dict['launches'][launch_no]['missions'])):
                if "id" in l_dict['launches'][launch_no]['missions'][mission_no]:
                    mission_id = l_dict['launches'][launch_no]['missions'][mission_no]['id']
                    mission = get_info("https://launchlibrary.net/1.1/mission/%d" % mission_id)
                    l_dict['launches'][launch_no]['missions'][mission_no]['details'] = mission['missions'][0]
        # Get rocket details if they exist
        if l_dict['launches'][launch_no]['rocket']['id']:
                    rocket_id = l_dict['launches'][launch_no]['rocket']['id']
                    rocket = get_info("https://launchlibrary.net/1.1/rocket/%d" % rocket_id)
                    l_dict['launches'][launch_no]['rocket']['details'] = rocket
    return l_dict


def give_names_to_ids(l_dict):
    status_name_dict = get_info("https://launchlibrary.net/1.1/launchstatus")
    agency_type_dict = get_info("https://launchlibrary.net/1.1/agencytype")
    mission_type_dict = get_info("https://launchlibrary.net/1.1/missiontype")
    for launch_no in xrange(len(l_dict['launches'])):
        # Translate launch status ID to descriptive string
        new_type_s = translate_type(l_dict['launches'][launch_no]['status'], status_name_dict)
        l_dict['launches'][launch_no]['status'] = new_type_s
        for mission_no in xrange(len(l_dict['launches'][launch_no]['missions'])):
            # Translate mission type(s) ID to descriptive string(s)
            new_type_m = translate_type(l_dict['launches'][launch_no]['missions'][mission_no]['details']['type'], mission_type_dict)
            l_dict['launches'][launch_no]['missions'][mission_no]['details']['type'] = new_type_m
            if 'agencies' in l_dict['launches'][launch_no]['missions'][mission_no]['details']:
                for agency_no in xrange(len(l_dict['launches'][launch_no]['missions'][mission_no]['details']['agencies'])):
                    # Translate mission agency type(s) ID to descriptive string(s)
                    new_type_a = translate_type(l_dict['launches'][launch_no]['missions'][mission_no]['details']['agencies'][agency_no]['type'], agency_type_dict)
                    l_dict['launches'][launch_no]['missions'][mission_no]['details']['agencies'][agency_no]['type'] = new_type_a
        for pad_no in xrange(len(l_dict['launches'][launch_no]['location']['pads'])):
            for agency_no in xrange(len(l_dict['launches'][launch_no]['location']['pads'][pad_no]['agencies'])):
                # Translate pad agency type(s) ID to descriptive string(s)
                new_type_a = translate_type(l_dict['launches'][launch_no]['location']['pads'][pad_no]['agencies'][agency_no]['type'], agency_type_dict)
                l_dict['launches'][launch_no]['location']['pads'][pad_no]['agencies'][agency_no]['type'] = new_type_a
        for agency_no in xrange(len(l_dict['launches'][launch_no]['rocket']['agencies'])):
            # Translate rocket agency type(s) ID to descriptive string(s)
            new_type_a = translate_type(l_dict['launches'][launch_no]['rocket']['agencies'][agency_no]['type'], agency_type_dict)
            l_dict['launches'][launch_no]['rocket']['agencies'][agency_no]['type'] = new_type_a
    return l_dict


# Other stuff ==========================================================

def get_info(url):
    """ Performs an HTTP GET from the target URL, fixes it, and evaluates it
    :param conn: active_HTTP_connection (ie. httplib.HTTPConnection(ip_address))
    :param url: target_url
    :return: evaluated_data
    """
    try:
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError:
            st_url = url.split("//")[1]
            st_url2 = st_url.split("/")[0]
            conn = httplib.HTTPConnection(st_url2)
            conn.request("GET", url)
            response = conn.getresponse()
        html = response.read()
        parsed = json.loads(html)
        str_conv = byteify(parsed)
    except:
        str_conv = {'Error': 'Unable to process request'}
    return str_conv


def translate_type(type_int, trans_dict):
    """ Takes a type id integer and returns its corresponding name (and description if there is one)
    :param type_int: type_id_as_int
    :param trans_dict: dictionary_with_translation_terms
    :return: corresponding_name_of_type_as_string
    """
    new_name = trans_dict['types'][type_int - 1]['name']
    if 'description' in trans_dict['types'][type_int-1]:
        newdesc = trans_dict['types'][type_int - 1]['description']
        new_name = new_name + ": " + newdesc
    return new_name


def breakout(dictionary, indent_level=0, only=0):
    """ Crawls recursively through a dictionary that contains other dictionaries or lists as values
    Displays all dictionary keys and/or values with tabbed levels
    :param dictionary: any_dictionary
    :param indent_level: starting_indent_level
    :param only: 0=keys_and_values 1=keys_only 2=values_only
    :return: None
    """
    for k, v in dictionary.iteritems():
        if type(v) is dict:
            if only != 2:
                print "\t" * indent_level, "['%s']" % k
            breakout(v, indent_level + 1, only=only)
        elif type(v) is list:
            if only != 2:
                print "\t" * indent_level, "['%s']" % k
            for item in xrange(len(v)):
                if only != 2:
                    print "\t" * (indent_level+1), "[%d]" % item
                breakout(v[item], indent_level + 2, only=only)
        else:
            if only == 1:
                print "\t" * indent_level, "['%s']" % k
            elif only == 2:
                print "\t" * indent_level, v
            else:
                print "\t" * indent_level, "['%s']" % k, (" " * (16 - len(k))), v


def byteify(input):
    """
    Borrowed from https://stackoverflow.com/questions/956867/
    how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
    """
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def open_link(url="http://www.google.com"):
    webbrowser.open(url)


# ______________________________________________________________________
# ======================================================================


if __name__ == "__main__":
    while True:
        a = raw_input("\n1 - Keys and Values\n2 - Keys\n3 - Values\n0 - Exit\n\nSelection: ")
        if a == "2":
            only_sel = 1
        elif a == "3":
            only_sel = 2
        elif a == "0":
            break
        else:
            only_sel = 0
        b = int(raw_input("Number of launches to retrieve: "))
        try:
            launch_d = get_launches(number_of_launches=b)
        except TypeError:
            launch_d = get_launches()
        for launch_number in xrange(len(launch_d['launches'])):
            name = launch_d['launches'][launch_number]['name']
            name_no = "Launch %d: %s" % ((launch_number+1), name)
            print '\n\n' + ('-' * 72)
            t_split = (((72-len(name_no))/2)*"-")
            msg = "%s %s %s" % (t_split, name_no, t_split)
            print msg[:72]
            countdown = "T - %s" % get_countdown(launch_d['launches'][launch_number]['net'])
            c_split = (((72-len(countdown))/2)*"-")
            msg = "%s %s %s" % (c_split, countdown, c_split)
            print msg[:72]
            net = "NET: %s" % convert_from_utc(launch_d['launches'][launch_number]['net'])
            n_split = (((72-len(net))/2)*"-")
            msg = "%s %s %s" % (n_split, net, n_split)
            print msg[:72]
            print ('-' * 72) + '\n'
            indent = 0
            breakout((launch_d['launches'][launch_number]), indent, only=only_sel)
        print '\n\n' + ('*' * 72)


# ______________________________________________________________________
# ======================================================================
