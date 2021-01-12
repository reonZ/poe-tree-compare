const cardTemplate = document.getElementById('card')
const masteryCardTemplate = document.getElementById('mastery-card')
const addedBlock = document.getElementById('added')
const removedBlock = document.getElementById('removed')
const modifiedBlock = document.getElementById('modified')

function displayNode(block, node, version) {
    const template = node.mastery ? masteryCardTemplate : cardTemplate
    const card = template.content.cloneNode(true)

    card.querySelector('.name').textContent = node.name

    const cardBlock = card.querySelector('.card')
    if (node.keystone) cardBlock.classList.add('keystone')

    if (!node.mastery) {
        const statsBlock = card.querySelector('.stats')
        for (const stat of node.stats) {
            const li = document.createElement('li')
            li.textContent = stat
            statsBlock.appendChild(li)
        }

        if (node.reminder) {
            cardBlock.classList.add('tooltip')
            cardBlock.setAttribute('data-tooltip', node.reminder.join('\n'))
        }
    }

    const icon = card.querySelector('.icon')
    const coords = node.sprite.coords
    icon.style.backgroundImage = `url("/data/${version}/assets/${node.sprite.filename}")`
    icon.style.backgroundPosition = `-${coords.x}px -${coords.y}px`
    icon.style.width = `${coords.w}px`
    icon.style.height = `${coords.h}px`

    block.appendChild(card)
}

if (data.added.length === 0) {
    addedBlock.style.display = 'none'
} else {
    for (const node of data.added) {
        displayNode(addedBlock, node, data.new)
    }
}

if (data.removed.length === 0) {
    removedBlock.style.display = 'none'
} else {
    for (const node of data.removed) {
        displayNode(removedBlock, node, data.old)
    }
}

if (data.modified.length === 0) {
    modifiedBlock.style.display = 'none'
} else {
    for (const nodes of data.modified) {
        displayNode(modifiedBlock, nodes.old, data.old)
        displayNode(modifiedBlock, nodes.new, data.new)
    }
}
