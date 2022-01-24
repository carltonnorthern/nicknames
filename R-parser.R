name_lookup <- function(name, filepath = "names.csv"){

  #### documentation ####

  # Look up name(s) in a given .csv file of full and diminutive names.  Values
  # returned are a list of names related to the inputted name(s).
  # Examples:
  #     name_lookup("greg")
  #         full_name diminutive_1 diminutive_2
  #         "gregory"       "greg"       "gory"
  #
  #     name_lookup(c("greg", "genevieve"))
  #     [[1]]
  #        full_name diminutive_1 diminutive_2
  #        "gregory"       "greg"       "gory"
  #     [[2]]
  #        full_name diminutive_1 diminutive_2 diminutive_3
  #        "genevieve"       "jean"        "eve"      "jenny"
  #
  #     name_lookup(c("greg", "adele", "xzy"))
  #     [[1]]
  #        full_name diminutive_1 diminutive_2
  #        "gregory"       "greg"       "gory"
  #
  #     [[2]]
  #       full_name diminutive_1
  #       "allen"         "al"
  #
  #     Warning message:
  #     In name_lookup(c("greg", "allen", "xzy")) : xzy not found in database
  #
  # Values:
  #     name (string, list): a list of names to look up
  #     filepath (string): location of names database, defaults to 'names.csv'


  #### regularize inputs ####

  if (is.character(name) != TRUE) {
    stop("name must be a character string")
  }

  name <- tolower(name)

  #### read in names data from csv ####

  names_df <- read.csv(filepath, header = FALSE)

  #### name the columns in names_df ####

  names(names_df)[names(names_df) == "V1"] <- "full_name"
  names(names_df)[2:length(names(names_df))] <-
    paste0("diminutive_", seq(1, length(names_df) - 1, 1))

  #### locate rows in names_df corresponding to desired name(s) ####

  names_df_cut <-
    names_df[which(apply(names_df, 1, function(row)
      any(row %in% c(name)))), ]

  if (nrow(names_df_cut) < 1) {
    stop("name not in database")
  }

  #### convert names_df_cut to named list and clean ####

  names_df_cut <- apply(names_df_cut, 1, as.list)
  names_list <- Map(unlist, names_df_cut)

  #### order list to match input order ####

  for (i in seq(1, length(names(names_list)))) {
    names(names_list)[i] <-
      name[lapply(names_list, function(x)
        name %in% x)[[i]]]
  }

  name_ordered <- ordered(name, levels = name)
  names_list <-
    names_list[order(match(names(names_list), name_ordered))]

  names(names_list) <- NULL

  names_list <- lapply(names_list, function(x)
    x[nzchar(x)])

  #### return ####
  if (length(names_list) == 1) {
    names_list <- unlist(names_list)
  }

  for (i in seq(1, length(name))) {
    if (name[i] %in% unlist(names_list) == FALSE) {
      warning(paste0(name[i], " not found in database"))
    }
  }

  return(names_list)

}
