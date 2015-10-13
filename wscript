# -*- mode: python; coding: utf-8; -*-

import waflib

def options(ctx):
    ctx.load('tex')

def configure(ctx):
    ctx.load('tex')
    ctx.load('open', tooldir='waf-tools')
    # The current version of Waf doesn't directly support LuaTeX, but we can
    # override the PDFLATEX variable which works fine.
    ctx.env.PDFLATEX = ctx.find_program('lualatex')

class OpenContext(waflib.Build.BuildContext):
    """opens the resume PDF"""
    cmd = 'open'

def build(ctx):
    tex_node = ctx.path.find_resource('document.tex')
    pdf_node = tex_node.change_ext('.pdf')
    ctx(features='tex',
        type='pdflatex',
        source=tex_node,
        outs='pdf',
        # prompt=0 enables batch mode, which disables the avalanche of output
        # normally produced by LaTeX.
        prompt=0)

    if ctx.cmd == 'open':
        def _open(ctx):
            ctx.open_file(pdf_node)
        ctx.add_post_fun(_open)
