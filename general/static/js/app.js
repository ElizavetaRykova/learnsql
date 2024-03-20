document.addEventListener('DOMContentLoaded', () => {

    const tabs = () => {
        const head = document.querySelector('.result__header')
        const body = document.querySelector('.result__body')

    const getActiveTabName = () => { 
        return head.querySelector('.result__tab-header_active').dataset.tab
    }

    const setActiveContent = () => { 
        if (body.querySelector('.result__tab-content_active')) {
          body.querySelector('.result__tab-content_active').classList.remove('result__tab-content_active')
        }
        body.querySelector(`[data-tab=${getActiveTabName()}]`).classList.add('result__tab-content_active') 
    }

    if (!head.querySelector('.result__tab-header_active')) {
        head.querySelector('.result__tab-header').classList.add('result__tab-header_active')
    }
    setActiveContent(getActiveTabName())

    head.addEventListener('click', e => {
      const caption = e.target.closest('.result__tab-header')
      if (!caption) return
      if (caption.classList.contains('result__tab-header_active')) return

      if (head.querySelector('.result__tab-header_active')) {
        head.querySelector('.result__tab-header_active').classList.remove('result__tab-header_active')
      }

      caption.classList.add('result__tab-header_active')

      setActiveContent(getActiveTabName())
    })
  }

  tabs()

})

console.log('test')