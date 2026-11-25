import web

render = web.template.render('mvc/views/publico', base='template')

class Index:

    def GET(self):
        return render.index() # type: ignore