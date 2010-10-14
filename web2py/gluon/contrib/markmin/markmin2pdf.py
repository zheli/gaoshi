"""
Created by Massimo Di Pierro
Licese BSD
"""

import subprocess
import os
import os.path
import re
import sys
from tempfile import mkstemp, mkdtemp, NamedTemporaryFile
from markmin2latex import markmin2latex

__all__ = ['markmin2pdf']
    
def removeall(path):

    ERROR_STR= """Error removing %(path)s, %(error)s """
    def rmgeneric(path, __func__):
        try:
            __func__(path)
        except OSError, (errno, strerror):
            print ERROR_STR % {'path' : path, 'error': strerror }

    files=[path]

    while files: 
        file=files[0]
        if os.path.isfile(file):
            f=os.remove
            rmgeneric(file, os.remove)
            del files[0]
        elif os.path.isdir(file):
            nested = os.listdir(file)
            if not nested:
                rmgeneric(file, os.rmdir)
                del files[0]
            else:
                files = [os.path.join(file,x) for x in nested] + files


def latex2pdf(latex, pdflatex='pdflatex', passes=3):
    """
    calls pdflatex in a tempfolder
    
    Arguments:
    
    - pdflatex: path to the pdflatex command. Default is just 'pdflatex'.
    - passes:   defines how often pdflates should be run in the texfile.
    """
    
    pdflatex=pdflatex
    passes=passes
    warnings=[]
    
    # setup the envoriment
    tmpdir = mkdtemp()
    texfile = open(tmpdir+'/test.tex','wb')
    texfile.write(latex)
    texfile.seek(0)
    texfile.close()
    texfile = os.path.abspath(texfile.name)

    # start doing some work
    for i in range(0, passes):
        logfd,logname = mkstemp()
        outfile=os.fdopen(logfd)
        ret = subprocess.call([pdflatex,
                               '-interaction=nonstopmode',
                               '-output-format', 'pdf',
                               '-output-directory', tmpdir,
                               texfile],
                              cwd=os.path.dirname(texfile), stdout=outfile, 
                              stderr=subprocess.PIPE)        
        outfile.close()
        re_errors=re.compile('^\!(.*)$',re.M)
        re_warnings=re.compile('^LaTeX Warning\:(.*)$',re.M)
        loglines=open(logname).read()
        errors=re_errors.findall(loglines)
        warnings=re_warnings.findall(loglines)
        os.unlink(logname)

    pdffile=texfile.rsplit('.',1)[0]+'.pdf'
    if os.path.isfile(pdffile):
        data = open(pdffile,'rb').read()
    else:
        data = None
    removeall(tmpdir)
    return data, warnings, errors
    

def markmin2pdf(text, image_mapper=lambda x: None):
    return latex2pdf(markmin2latex(text,image_mapper=image_mapper))


if __name__ == '__main__':
    import sys
    import doctest
    import markmin2html
    if sys.argv[1:2]==['-h']:
        data, warnings, errors = markmin2pdf(markmin2html.__doc__)
        if errors:
            print 'ERRORS:'+'\n'.join(errors)
            print 'WARNGINS:'+'\n'.join(warnings)
        else:
            print data
    elif len(sys.argv)>1:
        data, warnings, errors = markmin2pdf(open(sys.argv[1],'rb').read())
        if errors:
            print 'ERRORS:'+'\n'.join(errors)
            print 'WARNGINS:'+'\n'.join(warnings)
        else:
            print data
    else:
        doctest.testmod()
