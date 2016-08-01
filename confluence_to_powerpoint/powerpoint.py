from pptx import Presentation
import os


def make_presentation(target_name, statuses):
    if os.path.exists('template.pptx'):
        prs = Presentation('template.pptx')
    else:
        prs = Presentation()
    bullet_slide_layout = prs.slide_layouts[1]

    for status in statuses:
        slide = prs.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes

        title_shape = shapes.title
        body_shape = shapes.placeholders[1]

        title_shape.text = status['team']

        tf = body_shape.text_frame
        tf.text = status['RAG']

        p = tf.add_paragraph()
        p.text = status['summary']
        p.level = 1

    prs.save(target_name)