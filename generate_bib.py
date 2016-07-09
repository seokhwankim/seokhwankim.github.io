import sqlite3
import re
import datetime

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

db = sqlite3.connect('profile.db')
c = db.cursor()

db = BibDatabase()
db.entries = []

id_dict = {}

c.execute('SELECT title, authors, journal, journal_abbr, volume, pages, month, year FROM journal_paper WHERE locale = "international" ORDER BY year, month')
for row in c:
    title, authors, journal, journal_abbr, volume, pages, month, year = row

    title_kwd = None
    authors_kwd = None
    journal_kwd = None

    bib_obj = {'ENTRYTYPE': 'article'}
    if title is not None:
        bib_obj['title'] = title
        for word in re.split('[^A-Za-z0-9]', title):
            word = word.lower()
            if word != 'a' and word != 'the' and word != 'an':
                title_kwd = word
                break
            
    if authors is not None:
        bib_obj['author'] = ' AND '.join(authors.split('|'))
        author_kwd = authors.split('|')[0].split(' ')[-1].lower()

    if journal is not None:
        bib_obj['journal'] = journal

    if journal_abbr is not None and journal_abbr != '':
        journal_kwd = journal_abbr
        
    if volume is not None and volume != '':
        bib_obj['volume'] = str(volume)
    if pages is not None and pages != '':
        bib_obj['pages'] = pages.replace('-', '--')
    if year is not None:
        bib_obj['year'] = str(year)
    if month is not None:
        m = re.match('^([0-9]+)-([0-9]+)$', month)
        if m:
            dateobj = datetime.date(2000, int(m.group(1)), 1)
            mon1 = dateobj.strftime('%b')
            dateobj = datetime.date(2000, int(m.group(2)), 1)
            mon2 = dateobj.strftime('%b')
            bib_obj['month'] = ', %s-%s' % (mon1, mon2)
            month = int(m.group(1))
        else:
            m = re.match('^[0-9]+$', month)
            if m:
                dateobj = datetime.date(2000, int(month), 1)
                mon = dateobj.strftime('%b')
                bib_obj['month'] = mon
                month = int(month)

    if journal_kwd is not None:
        bib_id = '%s%s%s%s' % (author_kwd, journal_kwd, year, title_kwd)
    else:
        bib_id = '%s%s%s' % (author_kwd, year, title_kwd)

    if bib_id in id_dict:
        raise

    id_dict[bib_id] = True

    bib_obj['ID'] = bib_id
    print bib_id
    db.entries.append(bib_obj)
        
c.execute('SELECT title, authors, conference, conference_abbr, volume, pages, month, year, city FROM conference_paper WHERE locale = "international" ORDER BY year, month')
for row in c:
    title, authors, conference, conference_abbr, volume, pages, month, year, city = row
    bib_obj = {'ENTRYTYPE': 'inproceedings'}

    title_kwd = None
    authors_kwd = None
    conf_kwd = None

    if title is not None:
        bib_obj['title'] = title
        for word in re.split('[^A-Za-z0-9]', title):
            word = word.lower()
            if word != 'a' and word != 'the' and word != 'an':
                title_kwd = word
                break

    if authors is not None:
        bib_obj['author'] = ' AND '.join(authors.split('|'))
        author_kwd = authors.split('|')[0].split(' ')[-1].lower()

    if conference is not None:
        bib_obj['booktitle'] = 'Proceedings of %s' % (conference,)
        if conference_abbr is not None:
            m = re.match('^(.+) \'?[0-9]+$', conference_abbr)
            if m:
                conference_abbr = m.group(1)

            bib_obj['booktitle'] += ' (%s)' % (conference_abbr,)
            conf_kwd = re.split('[^A-Za-z0-9]', conference_abbr)[-1]

    if volume is not None and volume != '':
        bib_obj['volume'] = str(volume)
    if pages is not None and pages != '':
        bib_obj['pages'] = pages.replace('-', '--')
    if year is not None:
        bib_obj['year'] = str(year)
    if month is not None:
        month = str(month)
        m = re.match('^([0-9]+)-([0-9]+)$', month)
        if m:
            dateobj = datetime.date(2000, int(m.group(1)), 1)
            mon1 = dateobj.strftime('%b')
            dateobj = datetime.date(2000, int(m.group(2)), 1)
            mon2 = dateobj.strftime('%b')
            bib_obj['month'] = ', %s-%s' % (mon1, mon2)
            month = int(m.group(1))
        else:
            m = re.match('^[0-9]+$', month)
            if m:
                dateobj = datetime.date(2000, int(month), 1)
                mon = dateobj.strftime('%b')
                bib_obj['month'] = mon
                month = int(month)

    if conf_kwd is not None:
        bib_id = '%s%s%s%s' % (author_kwd, conf_kwd, year, title_kwd)
    else:
        bib_id = '%s%s%s' % (author_kwd, year, title_kwd)

    if bib_id in id_dict:
        raise

    id_dict[bib_id] = True

    bib_obj['ID'] = bib_id
    print bib_id
    db.entries.append(bib_obj)

writer = BibTexWriter()
with open('seokhwankim.bib', 'w') as bibfile:
    bibfile.write(writer.write(db))
