from yattag import Doc, indent
import sqlite3
import datetime
import re
import codecs

db = sqlite3.connect('profile.db')
c = db.cursor()

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')
with tag('html', lang='en'):
    header_info = {}
    c.execute('SELECT field, content FROM header')
    for row in c:
        field, content = row
        header_info[field] = content

    with tag('head'):
        doc.asis('<meta charset="utf-8">')
        doc.asis('<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />')
        doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
        if 'name' in header_info:
            with tag('title'):
                text(header_info['name'])
        doc.asis('<link href="css/bootstrap.min.css" rel="stylesheet">')
        doc.asis('<link href="css/font-awesome.css" rel="stylesheet">')
        doc.asis('<link href="css/main.css" rel="stylesheet">')

    with tag('body'):
        with tag('div', klass='container'):

            # HEADER
            with tag('div', klass='row'):
                with tag('div', klass='col-xs-12'):
                    with tag('div', id='photo-header', klass='text-center'):
                        with tag('div', id='photo'):
                            if 'photo' in header_info:
                                doc.stag('img', src=header_info['photo'], alt='photo')
                        with tag('div', id='text-header'):
                            with tag('h1'):
                                if 'name' in header_info:
                                    text(header_info['name'])
                                if 'title' in header_info:
                                    text(' ')
                                    with tag('sup'):
                                        text(header_info['title'])
                                    doc.stag('br')
                                if 'position' in header_info:
                                    text(header_info['position'])
                                    if 'affiliation' in header_info:
                                        text(', ')
                                        if 'affiliation_link' in header_info:
                                            with tag('a', href=header_info['affiliation_link']):
                                                text(header_info['affiliation'])
                                        else:
                                            text(header_info['affiliation'])

            # CONTACT
            contact_info = {}
            c.execute('SELECT field, content FROM contact')
            for row in c:
                contact_info[row[0]] = row[1]

#            with tag('div', klass='row'):
#                with tag('div', klass='col-xs-12'):
            with tag('div', klass='box clearfix'):
                with tag('h2'):
                    text('Contact')
                if 'address' in contact_info:
                    with tag('div', klass='contact-item'):
                        doc.asis('<div class="icon pull-left text-center"><span class="fa fa-building-o fa-fw"></span></div>')
                        with tag('div', klass='description pull-right'):
                            text(contact_info['address'])
                with tag('div', klass='row'):
                    if 'phone' in contact_info:
                        with tag('div', klass='col-xs-6'):
                            with tag('div', klass='contact-item'):
                                doc.asis('<div class="icon pull-left text-center"><span class="fa fa-phone fa-fw"></span></div>')
                                with tag('div', klass='description pull-right'):
                                    text(contact_info['phone'])
                    if 'mobile' in contact_info:
                        with tag('div', klass='col-xs-6'):
                            with tag('div', klass='contact-item'):
                                doc.asis('<div class="icon pull-left text-center"><span class="fa fa-mobile fa-fw"></span></div>')
                                with tag('div', klass='description pull-right'):
                                    text(contact_info['mobile'])
                with tag('div', klass='row'):
                    if 'email' in contact_info:
                        with tag('div', klass='col-xs-6'):
                            with tag('div', klass='contact-item'):
                                doc.asis('<div class="icon pull-left text-center"><span class="fa fa-envelope fa-fw"></span></div>')
                                with tag('div', klass='description pull-right'):
                                    doc.stag('img', src=contact_info['email'])
                    if 'website' in contact_info:
                        with tag('div', klass='col-xs-6'):
                            with tag('div', klass='contact-item'):
                                doc.asis('<div class="icon pull-left text-center"><span class="fa fa-home fa-fw"></span></div>')
                                with tag('div', klass='description pull-right'):
                                    with tag('a', href=contact_info['website']):
                                        text(contact_info['website'])
                with tag('div', klass='contact-item'):
                    doc.asis('<div class="icon pull-left text-center"><span class="fa fa-file-o fa-fw"></span></div>')
                    with tag('div', klass='description pull-right'):
                        with tag('a', href='cv/seokhwan-cv.pdf'):
                            text('Click HERE to download my curriculum vitae.')

            # RESEARCH INTEREST
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Research Interests')

                c.execute('SELECT keyword FROM research_interest')
                for row in c:
                    with tag('div', klass='interest'):
                        text(row[0])


            # EDUCATION
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Education')

                c.execute('SELECT degree, major, org, org_link, start_date, end_date, dissertation, advisor, committee, gpa FROM education ORDER BY start_date DESC')
                for row in c:
                    degree, major, org, org_link, start_date, end_date, dissertation, advisor, committee, gpa = row

                    with tag('div', klass='education clearfix'):
                        with tag('div', klass='col-xs-3'):
                            if degree is not None:
                                with tag('div', klass='degree'):
                                    text(degree)
                            if start_date is not None and end_date is not None:
                                with tag('div', klass='year'):
                                    start_ym = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%b %Y')
                                    end_ym = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%b %Y')
                                    text('%s - %s' % (start_ym, end_ym))
                        with tag('div', klass='col-xs-9'):
                            if org is not None:
                                with tag('div', klass='where'):
                                    if org_link is not None:
                                        with tag('a', href=org_link):
                                            text(org)
                                    else:
                                        text(org)
                            if major is not None:
                                with tag('div', klass='major'):
                                    text(major)
                            if dissertation is not None or advisor is not None:
                                with tag('div', klass='description'):
                                    if dissertation is not None:
                                        text('Dissertation: %s' % (dissertation,))
                                        doc.stag('br')
                                    if advisor is not None:
                                        text('Advisor: %s' % (advisor,))


            # RESEARCH EXPERIENCES
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Research Experiences')

                c.execute('SELECT position, org, org_link, lab, dept, start_date, end_date, advisor FROM work ORDER BY start_date DESC')
                for row in c:
                    position, org, org_link, lab, dept, start_date, end_date, advisor = row

                    with tag('div', klass='job clearfix'):
                        with tag('div', klass='col-xs-3'):
                            if position is not None:
                                with tag('div', klass='profession'):
                                    text(position)
                            if start_date is not None:
                                with tag('div', klass='year'):
                                    start_ym = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%b %Y')
                                    if end_date is not None:
                                        end_ym = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%b %Y')
                                        text('%s - %s' % (start_ym, end_ym))
                                    else:
                                        text('%s -' % (start_ym,))
                        with tag('div', klass='col-xs-9'):
                            if org is not None:
                                with tag('div', klass='where'):
                                    if org_link is not None:
                                        with tag('a', href=org_link):
                                            text(org)
                                    else:
                                        text(org)
                            if dept is not None or lab is not None or advisor is not None:
                                with tag('div', klass='description'):
                                    if lab is not None:
                                        text(lab)
                                    if dept is not None:
                                        if lab is not None:
                                            text(',')
                                            doc.stag('br')
                                        text(dept)
                                    if advisor is not None:
                                        if lab is not None or dept is not None:
                                            doc.stag('br')
                                        text('Advisor: %s' % (advisor,))

            # TEACHING EXPERIENCES
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Teaching Experiences')

                c.execute('SELECT position, org, org_link, course_code, course, professor, year, semester FROM teaching ORDER BY year DESC')
                for row in c:
                    position, org, org_link, course_code, course, professor, year, semester = row
                    with tag('div', klass='job clearfix'):
                        with tag('div', klass='col-xs-3'):
                            if position is not None:
                                with tag('div', klass='profession'):
                                    text(position)
                            if year is not None:
                                with tag('div', klass='year'):
                                    if semester is not None:
                                        text('%s %d' % (semester, year))
                                    else:
                                        text('%d' % (year,))
                        with tag('div', klass='col-xs-9'):
                            if org is not None:
                                with tag('div', klass='where'):
                                    if org_link is not None:
                                        with tag('a', href=org_link):
                                            text(org)
                                    else:
                                        text(org)
                            if course_code is not None or course is not None or professor is not None:
                                with tag('div', klass='description'):
                                    if course_code is not None:
                                        text(course_code)
                                    if course is not None:
                                        if course_code is not None:
                                            text(', ')
                                        text(course)
                                    if professor is not None:
                                        if course_code is not None or course is not None:
                                            doc.stag('br')
                                        text('Professor: %s' % (professor,))

            # PROFESSIONAL EXPERIENCES
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Professional Experiences')

                c.execute('SELECT position, org, org_link, start_year, end_year FROM ACTIVITY ORDER BY start_year DESC')
                for row in c:
                    position, org, org_link, start_year, end_year = row

                    if start_year is not None:
                        with tag('div', klass='job clearfix'):
                            with tag('div', klass='col-xs-3'):
                                if position is not None:
                                    with tag('div', klass='profession'):
                                        text(position)
                                if start_year is not None:
                                    with tag('div', klass='year'):
                                        text('%d' % (start_year,))
                            with tag('div', klass='col-xs-9'):
                                if org is not None:
                                    with tag('div', klass='where'):
                                        if org_link is not None:
                                            with tag('a', href=org_link):
                                                text(org)
                                        else:
                                            text(org)

                review_list = []
                c.execute('SELECT org FROM ACTIVITY WHERE position = "Reviewer" ORDER BY org')
                for row in c:
                    review_list.append(row[0])

                if len(review_list) > 0:
                    with tag('div', klass='job clearfix'):
                        with tag('div', klass='col-xs-3'):
                            if position is not None:
                                with tag('div', klass='profession'):
                                    text('Reviewer')
                        with tag('div', klass='col-xs-9'):
                            with tag('div', klass='where'):
                                text(', '.join(review_list))

            # Preparing publication list
            pub_by_year = {}

            journal_id = 0
            c.execute('SELECT title, authors, journal, volume, pages, month, year, publisher_link, pdf_link, bib_link FROM journal_paper WHERE locale = "international" ORDER BY year, month')
            for row in c:
                title, authors, journal, volume, pages, month, year, publisher_link, pdf_link, bib_link = row
                journal_id += 1
                pub_obj = {'id': 'J%d' % (journal_id,)}
                if title is not None:
                    pub_obj['title'] = title
                if authors is not None:
                    pub_obj['author'] = authors.split('|')

                pub_obj['src'] = journal
                pub_obj['volume'] = volume
                pub_obj['pages'] = pages

                if month is not None:
                    m = re.match('^([0-9]+)-([0-9]+)$', month)
                    if m:
                        dateobj = datetime.date(2000, int(m.group(1)), 1)
                        mon1 = dateobj.strftime('%b')
                        dateobj = datetime.date(2000, int(m.group(2)), 1)
                        mon2 = dateobj.strftime('%b')
                        pub_obj['month'] = ', %s-%s' % (mon1, mon2)
                        month = int(m.group(1))
                    else:
                        m = re.match('^[0-9]+$', month)
                        if m:
                            dateobj = datetime.date(2000, int(month), 1)
                            mon = dateobj.strftime('%b')
                            pub_obj['month'] = mon
                            month = int(month)

                pub_obj['year'] = year

                pub_obj['publisher_link'] = publisher_link
                pub_obj['pdf_link'] = pdf_link
                pub_obj['bib_link'] = bib_link

                if year not in pub_by_year:
                    pub_by_year[year] = {}
                if month not in pub_by_year[year]:
                    pub_by_year[year][month] = []
                pub_by_year[year][month].insert(0, pub_obj)

            conference_id = 0
            c.execute('SELECT title, authors, conference, conference_abbr, volume, pages, month, year, city, conference_link, publisher_link, pdf_link, bib_link, slide_link, poster_link, rate, type FROM conference_paper WHERE locale = "international" ORDER BY year, month')
            for row in c:
                title, authors, conference, conference_abbr, volume, pages, month, year, city, conference_link, publisher_link, pdf_link, bib_link, slide_link, poster_link, rate, tp = row
                conference_id += 1
                pub_obj = {'id': 'C%d' % (conference_id,)}
                if title is not None:
                    pub_obj['title'] = title
                if authors is not None:
                    pub_obj['author'] = authors.split('|')

                pub_obj['src'] = ''
                if conference is not None:
                    today = datetime.date.today()
                    if year > today.year or (year == today.year and month > today.month):
                        pub_obj['src'] += 'To appear in '
                    pub_obj['src'] += 'Proceedings of %s' % (conference,)

                pub_obj['volume'] = volume
                pub_obj['pages'] = pages

                if conference_abbr is not None:
                    pub_obj['abbr'] = conference_abbr
                if conference_link is not None:
                    pub_obj['src_link'] = conference_link
                pub_obj['publisher_link'] = publisher_link
                pub_obj['pdf_link'] = pdf_link
                pub_obj['bib_link'] = bib_link
                pub_obj['slide_link'] = slide_link
                pub_obj['poster_link'] = poster_link

                if rate is not None:
                    pub_obj['rate'] = str(rate)
                pub_obj['type'] = tp
                pub_obj['city'] = city

                if month is not None:
                    dateobj = datetime.date(2000, int(month), 1)
                    mon = dateobj.strftime('%b')
                    pub_obj['month'] = mon
                    month = int(month)

                pub_obj['year'] = year

                if year not in pub_by_year:
                    pub_by_year[year] = {}
                if month not in pub_by_year[year]:
                    pub_by_year[year][month] = []
                pub_by_year[year][month].insert(0, pub_obj)

            # PUBLICATIONS
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Publications')

                for year in reversed(sorted(pub_by_year.keys())):
                    is_first = True
                    for month in reversed(sorted(pub_by_year[year].keys())):
                        for pub_obj in pub_by_year[year][month]:
                            is_journal = False
                            with tag('div', klass='publication clearfix'):
                                with tag('div', klass='col-xs-1'):
                                    if is_first:
                                        with tag('div', klass='year'):
                                            text(year)
                                        is_first = False
                                with tag('div', klass='col-xs-11'):
                                    if pub_obj['id'].startswith('J'):
                                        is_journal = True
                                        with tag('div', klass='pid_journal', style='display:inline'):
                                            text('[%s] ' % (pub_obj['id'],))
                                    elif pub_obj['id'].startswith('C'):
                                        with tag('div', klass='pid_conference', style='display:inline'):
                                            text('[%s] ' % (pub_obj['id'],))
                                    with tag('div', klass='title', style='display:inline'):
                                        text('%s.' % (pub_obj['title'],))

                                        if pub_obj['pdf_link'] is not None and len(pub_obj['pdf_link']) > 0:
                                            with tag('div', klass='link', style='display:inline'):
                                                with tag('a', href=pub_obj['pdf_link']):
                                                    text('[PDF]')
                                        elif pub_obj['publisher_link'] is not None and len(pub_obj['publisher_link']) > 0:
                                            with tag('div', klass='link', style='display:inline'):
                                                with tag('a', href=pub_obj['publisher_link']):
                                                    text('[link]')

                                        if 'bib_link' in pub_obj and pub_obj['bib_link'] is not None and len(pub_obj['bib_link']) > 0:
                                            with tag('div', klass='link', style='display:inline'):
                                                with tag('a', href=pub_obj['bib_link']):
                                                    text('[bib]')

                                        if 'slide_link' in pub_obj and pub_obj['slide_link'] is not None and len(pub_obj['slide_link']) > 0:
                                            with tag('div', klass='link', style='display:inline'):
                                                with tag('a', href=pub_obj['slide_link']):
                                                    text('[slides]')

                                        if 'poster_link' in pub_obj and pub_obj['poster_link'] is not None and len(pub_obj['poster_link']) > 0:
                                            with tag('div', klass='link', style='display:inline'):
                                                with tag('a', href=pub_obj['poster_link']):
                                                    text('[poster]')

                                    if pub_obj['author'] is not None:
                                        with tag('div', klass='author'):
                                            is_first = True
                                            for author in pub_obj['author']:
                                                if is_first is True:
                                                    is_first = False
                                                else:
                                                    text(', ')

                                                if author == header_info['name']:
                                                    with tag('span'):
                                                        text(author)
                                                else:
                                                    text(author)

                                    if pub_obj['src'] is not None:
                                        with tag('div', klass='book'):
                                            text(pub_obj['src'])
                                            if is_journal is True:
                                                if pub_obj['volume'] is not None:
                                                    text(', %s' % (pub_obj['volume'],))
                                                if pub_obj['pages'] is not None:
                                                    text(' (%s)' % (pub_obj['pages'],))
                                                if pub_obj['month'] is not None:
                                                    text(', %s' % (pub_obj['month'],))
                                                if pub_obj['year'] is not None:
                                                    text(' %s' % (pub_obj['year'],))
                                            else:
                                                if 'abbr' in pub_obj and len(pub_obj['abbr']) > 0:
                                                    text(' (')
                                                    if 'src_link' in pub_obj and len(pub_obj['src_link']) > 0:
                                                        with tag('a', href=pub_obj['src_link']):
                                                            text(pub_obj['abbr'])
                                                    else:
                                                        text(pub_obj['abbr'])
                                                    text(')')
                                                if 'volume' in pub_obj and len(str(pub_obj['volume'])) > 0:
                                                    text(', vol. %s' % (str(pub_obj['volume']),))
                                                if 'pages' in pub_obj and pub_obj['pages'] is not None and len(pub_obj['pages']) > 0:
                                                    text(', pp. %s' % (pub_obj['pages']),)
                                                if 'city' in pub_obj and pub_obj['city'] is not None and len(pub_obj['city']) > 0:
                                                    text(', %s' % (pub_obj['city'],))
                                                if 'month' in pub_obj and pub_obj['month'] is not None and len(pub_obj['month']) > 0:
                                                    text(', %s' % (pub_obj['month'],))
                                                if 'year' in pub_obj:
                                                    text(' %s.' % (pub_obj['year'],))
                                                if 'type' in pub_obj and pub_obj['type'] is not None and len(pub_obj['type']) > 0:
                                                    text(' (%s)' % (pub_obj['type'],))
                                                if 'rate' in pub_obj and pub_obj['rate'] is not None and len(pub_obj['rate']) > 0:
                                                    with tag('div', klass='rate', style='display:inline'):
                                                        text(' (%s%% acceptance)' % (pub_obj['rate'],))




            # PATENTS
            with tag('div', klass='box'):
                with tag('h2'):
                    text('Patents')

                patent_list = {}
                patent_id = 0
                c.execute('SELECT title_en, authors, reg_no, reg_date, file_no, file_date, country FROM patent WHERE type = "patent" AND title_en IS NOT NULL ORDER BY DATE(reg_date)')
                for row in c:
                    title_en, authors, reg_no, reg_date, file_no, file_date, country = row

                    if title_en is not None and len(title_en) > 0:
                        patent_id += 1
                        patent_obj = {}
                        patent_obj['title'] = title_en
                        patent_obj['authors'] = authors.split('|')
                        patent_obj['reg_no'] = reg_no
                        patent_obj['reg_date'] = reg_date
                        patent_obj['country'] = country

                        patent_list[patent_id] = patent_obj

                for patent_id in reversed(sorted(patent_list.keys())):
                    patent_obj = patent_list[patent_id]
                    with tag('div', klass='publication clearfix'):
                        with tag('div', klass='col-xs-12'):
                            with tag('div', klass='pid_patent', style='display:inline'):
                                text('[P%d] ' % (patent_id,))
                            with tag('div', klass='title', style='display:inline'):
                                text('%s.' % (patent_obj['title'],))

                            with tag('div', klass='author'):
                                is_first = True
                                for author in patent_obj['authors']:
                                    if is_first is True:
                                        is_first = False
                                    else:
                                        text(', ')

                                    if author == header_info['name']:
                                        with tag('span'):
                                            text(author)
                                    else:
                                        text(author)
                            with tag('div', klass='book'):
                                if 'reg_no' in patent_obj:
                                    text('Registration #%s' % (patent_obj['reg_no'],))
                                if 'country' in patent_obj and patent_obj['country'] is not None and len(patent_obj['country']) > 0:
                                    text(', %s' % (patent_obj['country'],))
                                if 'reg_date' in patent_obj:
                                    reg_date = datetime.datetime.strptime(patent_obj['reg_date'].replace(' ', ''), '%Y.%m.%d').strftime('%d %b %Y')
                                    text(', %s' % (reg_date,))
                                text('.')

            with tag('div', id='footer'):
                text('Last updated: %s' % (datetime.date.today()))
with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(indent(doc.getvalue()))
