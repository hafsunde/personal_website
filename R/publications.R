# Rendering helpers for data/publications.yml.
#
# publications.qmd uses pub_groups() for the full list; index.qmd uses
# selected_publications() for the home page. Nothing here needs touching when a
# paper lands — that is one entry in the YAML.

ME <- "Sunde, H.F."

esc <- function(x) {
  x <- gsub("&", "&amp;", x, fixed = TRUE)
  x <- gsub("<", "&lt;", x, fixed = TRUE)
  gsub(">", "&gt;", x, fixed = TRUE)
}

read_publications <- function(path = "data/publications.yml") {
  pubs <- yaml::read_yaml(path)
  stopifnot(is.list(pubs), length(pubs) > 0)
  pubs
}

# "Sunde, H.F., Eilertsen, E.M., & Torvik, F.A.", with his own name bolded.
pub_authors <- function(pub) {
  raw <- unlist(pub$authors)
  a <- esc(raw)
  a[raw == ME] <- paste0("<strong>", esc(ME), "</strong>")
  if (isTRUE(pub$et_al)) return(paste0(a[1], ", et al."))
  if (length(a) == 1) return(a)
  paste0(paste(a[-length(a)], collapse = ", "), ", &amp; ", a[length(a)])
}

# Labels for the editorial `links:` block. Unknown keys fall back to the key.
LINK_LABELS <- c(
  bluesky          = "Bluesky thread",
  bluesky_preprint = "Bluesky thread (preprint)",
  twitter          = "Twitter/X thread",
  twitter2         = "Twitter/X thread",
  twitter3         = "Twitter/X thread",
  preprint         = "Open-access preprint"
)

pub_links <- function(pub) {
  items <- character(0)
  if (!is.null(pub$doi)) {
    items <- c(items, sprintf(
      '<a class="pub-doi" href="https://doi.org/%s">doi:%s</a>', pub$doi, pub$doi
    ))
  }
  for (key in names(pub$links)) {
    label <- unname(LINK_LABELS[key])
    if (is.na(label)) label <- key
    items <- c(items, sprintf('<a href="%s">%s</a>', pub$links[[key]], esc(label)))
  }
  if (!length(items)) return("")
  paste0('<p class="pub-links">', paste(items, collapse = ""), "</p>")
}

pub_description <- function(pub) {
  if (is.null(pub$description)) return("")
  paste0('<p class="pub-description">', esc(pub$description), "</p>")
}

pub_html <- function(pub) {
  paste0(
    '<li class="pub">',
    '<p class="pub-title">', esc(pub$title), "</p>",
    '<p class="pub-meta">', pub_authors(pub), " (", pub$year, "). ",
    "<em>", esc(pub$venue), "</em>.</p>",
    pub_description(pub),
    pub_links(pub),
    "</li>"
  )
}

pub_list_html <- function(pubs) {
  if (!length(pubs)) return("")
  paste0(
    '<ul class="pub-list">',
    paste(vapply(pubs, pub_html, character(1)), collapse = ""),
    "</ul>"
  )
}

# Preprints first, then years descending. Order within a group is the order the
# entries appear in the YAML.
pub_groups <- function(pubs) {
  is_pre <- vapply(pubs, function(p) identical(p$type, "preprint"), logical(1))
  years <- vapply(pubs, function(p) as.integer(p$year), integer(1))
  groups <- list()
  if (any(is_pre)) groups[["Preprints"]] <- pubs[is_pre]
  for (y in sort(unique(years[!is_pre]), decreasing = TRUE)) {
    groups[[as.character(y)]] <- pubs[!is_pre & years == y]
  }
  groups
}

selected_publications <- function(pubs) {
  sel <- pubs[vapply(pubs, function(p) isTRUE(p$selected), logical(1))]
  sel[order(-vapply(sel, function(p) as.integer(p$year), integer(1)))]
}
