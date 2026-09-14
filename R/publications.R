# Rendering helpers for data/publications.yml.
#
# publications.qmd uses pub_groups() for the full list; index.qmd uses
# selected_html() for the selected-paper panels on the home page. Nothing here
# needs touching when a paper lands — that is one entry in the YAML.

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

# His authorship role on a paper. Sole first and last authorship are computed
# from author order; joint roles can't be, so they come from `authorship:`.
ROLE_LABELS <- c(
  "first"       = "First author",
  "last"        = "Last author",
  "joint-first" = "Joint first author",
  "joint-last"  = "Joint last author"
)

pub_role <- function(pub) {
  if (!is.null(pub$authorship)) {
    stopifnot(pub$authorship %in% names(ROLE_LABELS))
    return(pub$authorship)
  }
  if (isTRUE(pub$et_al)) return(NULL)
  a <- unlist(pub$authors)
  pos <- match(ME, a)
  if (is.na(pos) || length(a) < 2) return(NULL)
  if (pos == 1) return("first")
  if (pos == length(a)) return("last")
  NULL
}

pub_html <- function(pub) {
  role <- pub_role(pub)
  # Joint roles share the colour of their sole counterpart: pub-first or pub-last.
  li_class <- if (is.null(role)) "pub" else paste0("pub pub-", sub("^joint-", "", role))
  label <- if (is.null(role)) "" else paste0('<p class="pub-role">', ROLE_LABELS[[role]], "</p>")
  paste0(
    '<li class="', li_class, '">',
    label,
    '<p class="pub-title"><a href="https://doi.org/', pub$doi, '">', esc(pub$title), "</a></p>",
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

# Selected papers (home page). data/selected.yml sets the order and holds the
# editorial content; the reference itself comes from data/publications.yml.
read_selected <- function(path = "data/selected.yml") {
  sel <- yaml::read_yaml(path)
  stopifnot(is.list(sel), length(sel) > 0)
  sel
}

selected_html <- function(selected, pubs) {
  by_id <- setNames(pubs, vapply(pubs, function(p) p$id, character(1)))
  panels <- vapply(selected, function(s) {
    pub <- by_id[[s$id]]
    if (is.null(pub)) stop("data/selected.yml: no publication with id ", s$id)
    url <- paste0("https://doi.org/", pub$doi)
    abstract <- paste(vapply(s$abstract, function(sec) {
      heading <- if (is.null(sec$heading)) "" else paste0("<strong>", esc(sec$heading), ".</strong> ")
      paste0("<p>", heading, esc(sec$text), "</p>")
    }, character(1)), collapse = "")
    paste0(
      '<article class="selected-paper">',
      '<a class="selected-image" href="', url, '">',
      '<img src="', s$image, '" alt="First page of the published article" loading="lazy">',
      "</a>",
      '<div class="selected-body">',
      '<h3 class="selected-title"><a href="', url, '">', esc(pub$title), "</a></h3>",
      '<p class="pub-meta">', pub_authors(pub), " (", pub$year, "). ",
      "<em>", esc(pub$venue), "</em>.</p>",
      '<p class="selected-label">Abstract</p>',
      '<div class="selected-abstract">', abstract, "</div>",
      pub_links(pub),
      "</div>",
      "</article>"
    )
  }, character(1))
  paste0('<div class="selected-papers">', paste(panels, collapse = ""), "</div>")
}
