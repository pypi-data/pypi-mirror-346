from collections import defaultdict
from functools import lru_cache

from nexus import NexusWriter

from .CognateParser import CognateParser
from .tools import slugify, parse_parameter


def is_integer(x):
    try:
        int(x)
        return True
    except ValueError:
        return False



class Record(object):
    def __init__(self, **kwargs):
        defaults = ['ID', 'Language_ID', 'Language', 'Parameter_ID', 'Parameter', 'Item', 'Loan', 'Cognacy']
        for key in defaults:
            setattr(self, key, None)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __repr__(self):
        return "<Record %s - %s - %s - %s>" % (
            self.ID, self.Language, self.Parameter, self.Item
        )

    @property
    def is_loan(self):
        if self.Loan is None:
            return False
        elif isinstance(self.Loan, bool):
            return self.Loan
        elif isinstance(self.Loan, str):
            if self.Loan.lower() in ("", "false"):
                return False
            else:
                return True
        raise ValueError("should not happen: %r" % self.Loan)  # pragma: no cover
        
    def get_taxon(self):
        if self.Language_ID is None:
            return slugify(self.Language)
        elif is_integer(self.Language_ID):
            return "%s_%s" % (slugify(self.Language), str(self.Language_ID))
        else:
            return self.Language_ID


class NexusMaker(object):
    """
    data = list of Record instances
    cogparser = a specified CognateParser instance (default=None).
    remove_loans = remove loan words (default=True)
    unique_ids = keep record_ids for unique cognates (default=False)
    """
    def __init__(self, data=None, cogparser=None, remove_loans=True, unique_ids=False):
        self.remove_loans = remove_loans
        data = [] if data is None else data
        self._cognates = None
        self.languages = set()
        self.parameters = set()
        self.data = []
        
        for record in data:
            self.add(record)

        self.cogparser = cogparser if cogparser else CognateParser(strict=True, uniques=True)
        self.unique_ids = unique_ids

    def add(self, record):
        """Adds to record list and checks that we have the values we need"""
        if not isinstance(record, Record):
            raise ValueError("Should be a `Record` instance")
        
        # skip adding loans if remove_loans=False
        if self.remove_loans and record.is_loan:
            return
        
        
        if not hasattr(record, 'Language') or record.Language is None:
            raise ValueError("Record has no `Language` %r" % record)
        if not hasattr(record, 'Parameter') or record.Parameter is None:
            raise ValueError("Record has no `Parameter` %r" % record)
        
        self.languages.add(record.get_taxon())
        self.parameters.add(record.Parameter)
        
        self._cognates = None  # invalidate cognates to avoid a stale/incorrect cache
        self.data.append(record)
        return record

    def get_coglabel(self, record, value):
        return (record.Parameter, value)

    @lru_cache(maxsize=None)
    def _is_missing_for_parameter(self, language, parameter):
        """
        Returns True if the given `language` has no cognates for `parameter`
        """
        cogs = [
            c for c in self.cognates if c[0] == parameter and language in self.cognates[c]
        ]
        return len(cogs) == 0

    @property
    def cognates(self):
        if not self._cognates:
            # cognate sets (parameter, cogstate)
            self._cognates = defaultdict(set)
            # unique sets (language, parameter)
            uniques = {}
            # set of (language, parameter) pairs where a language already has a
            # cognate -- used for correct handling of uniques below.
            hascog = set()

            for rec in self.data:
                if self.remove_loans and rec.is_loan:  # pragma: no cover
                    #raise ValueError("%r is a loan!" % rec)
                    continue
                
                for cog in self.cogparser.parse_cognate(rec.Cognacy, rec.ID if self.unique_ids else None):
                    if self.cogparser.is_unique_cognateset(cog):
                        uniques[(rec.get_taxon(), rec.Parameter)] = cog
                    else:
                        # add cognate
                        self._cognates[self.get_coglabel(rec, cog)].add(
                            rec.get_taxon()
                        )
                        hascog.add((rec.get_taxon(), rec.Parameter))

            # now handle special casing of uniques.
            # 1. If the language already has an entry for the parameter
            # that is cognate, then do nothing (i.e. we have identified
            # the cognate forms, the new form is something else, but we don’t
            # care).
            #
            # 2. If none of the forms are cognate for that Parameter P then the
            # language is assigned ONE unique cognate set regardless of how many
            # records there are in the database for that parameter in that
            # language i.e. we know it’s evolved a new cognate set, and 
            # it could be any one of the other forms, but we don’t care which
            # form.
            for (lang, parameter) in sorted(uniques):
                if (lang, parameter) not in hascog:
                    cog = uniques[(lang, parameter)]
                    assert (parameter, cog) not in self._cognates
                    self._cognates[(parameter, cog)] = set([lang])
                    hascog.add((lang, parameter))
        return self._cognates

    @lru_cache(maxsize=1024)
    def make_slug(self, parameter):
        return slugify(parameter.lower().replace(" ", "").replace("_", ""))

    def make_coglabel(self, parameter, cog):
        return "%s_%s" % (self.make_slug(parameter), cog)

    def make(self):
        nex = NexusWriter()
        for cog in sorted(self.cognates):
            if self.cogparser.is_unique_cognateset(cog[1]):
                assert len(self.cognates[cog]) == 1, \
                    "Cognate (%s, %s) should be unique but has multiple members" % cog
            else:
                assert len(self.cognates[cog]) >= 1, \
                    "%s = %r" % (cog, self.cognates[cog])

            for lang in self.languages:
                if lang in self.cognates[cog]:
                    value = '1'
                elif self._is_missing_for_parameter(lang, cog[0]):
                    value = '?'
                else:
                    value = '0'

                nex.add(slugify(lang), self.make_coglabel(*cog), value)
        nex = self._add_ascertainment(nex)  # handle ascertainment
        return nex

    def _add_ascertainment(self, nex):  # subclass this to extend
        return nex

    def display_cognates(self):  # pragma: no cover
        for cog in sorted(self.cognates):
            print(cog, sorted(self.cognates[cog]))

    def write(self, nex=None, filename=None):
        if nex is None:
            nex = self.make()

        if filename is None:
            return nex.write(charblock=True)
        else:
            return nex.write_to_file(filename, charblock=True)


class NexusMakerAscertained(NexusMaker):
    ASCERTAINMENT_LABEL = '_ascertainment_0'

    def _add_ascertainment(self, nex):
        """Adds an overall ascertainment character"""
        if self.ASCERTAINMENT_LABEL in nex.data:
            raise ValueError(
                'Duplicate ascertainment key "%s"!' % self.ASCERTAINMENT_LABEL
            )

        for lang in self.languages:
            nex.add(lang, self.ASCERTAINMENT_LABEL, '0')
        return nex


class NexusMakerAscertainedParameters(NexusMaker):

    ASCERTAINMENT_LABEL = '0ascertainment'

    def _add_ascertainment(self, nex):
        """Adds an ascertainment character per parameter"""
        for parameter in self.parameters:
            coglabel = self.make_coglabel(parameter, self.ASCERTAINMENT_LABEL)
            if coglabel in nex.data:  # pragma: no cover
                raise ValueError('Duplicate ascertainment key "%s"!' % coglabel)

            for lang in self.languages:
                if self._is_missing_for_parameter(lang, parameter):
                    nex.add(slugify(lang), coglabel, '?')
                else:
                    nex.add(slugify(lang), coglabel, '0')
        return nex

    def _get_characters(self, nex, delimiter="_"):
        """Find all characters"""
        chars = defaultdict(list)
        for site_id, label in enumerate(sorted(nex.data.keys())):
            parameter, cogid = parse_parameter(label, delimiter)
            chars[parameter].append(site_id)
        return chars

    def _is_sequential(self, siteids):
        return sorted(siteids) == list(range(min(siteids), max(siteids) + 1))

    def create_assumptions(self, nex):
        chars = self._get_characters(nex)
        buffer = []
        buffer.append("begin assumptions;")
        for char in sorted(chars):
            siteids = sorted(chars[char])
            # increment by one as these are siteids not character positions
            siteids = [s + 1 for s in siteids]
            assert self._is_sequential(siteids), 'char is not sequential %s' % char
            if min(siteids) == max(siteids):  # pragma: no cover
                # should not happen as we always have +1 for the
                # ascertainment character
                out = "\tcharset %s = %d;" % (char, min(siteids))
            else:
                out = "\tcharset %s = %d-%d;" % (char, min(siteids), max(siteids))
            buffer.append(out)
        buffer.append("end;")
        return buffer

    def write(self, nex=None, filename=None):
        if nex is None:
            nex = self.make()

        if filename is None:
            return nex.write(charblock=True) + "\n\n" + "\n".join(self.create_assumptions(nex))
        else:  # pragma: no cover
            nex.write_to_file(filename, charblock=True)
            with open(filename, 'a', encoding='utf8') as handle:
                handle.write("\n")
                for line in self.create_assumptions(nex):
                    handle.write(line + "\n")
                handle.write("\n")
            return True
