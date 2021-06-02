"""
    Fichier : gestion_droits_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_FILMS import obj_mon_application
from APP_FILMS.database.connect_db_context_manager import MaBaseDeDonnee
from APP_FILMS.erreurs.exceptions import *
from APP_FILMS.erreurs.msg_erreurs import *

"""
    Nom : personnes_droits_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /personnes_droits_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@obj_mon_application.route("/personnes_droits_afficher/<int:id_droit_sel>", methods=['GET', 'POST'])
def personnes_droits_afficher(id_droit_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as Exception_init_droits_afficher:
                code, msg = Exception_init_droits_afficher.args
                flash(f"{error_codes.get(code, msg)} ", "danger")
                flash(f"Exception _init_personnes_droits_afficher problème de connexion BD : {sys.exc_info()[0]} "
                      f"{Exception_init_droits_afficher.args[0]} , "
                      f"{Exception_init_droits_afficher}", "danger")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_droits_afficher_data = """SELECT t_personne.id_personne, t_personne.Nom_personne, t_personne.Prenom_personne, t_personne.Date_naissance_personne, t_personne.Adresse_mail_personne, t_personne.MDP_personne FROM t_personne ORDER BY id_personne ASC"""
                if id_droit_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_droits_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_droit_selected_dictionnaire = {"value_id_droit_selected": id_droit_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_droits_afficher_data += """ HAVING id_droit= %(value_id_droit_selected)s"""

                    mc_afficher.execute(strsql_droits_afficher_data, valeur_id_droit_selected_dictionnaire)

                # Récupère les données de la requête.
                data_droits_afficher = mc_afficher.fetchall()
                print("data_droits ", data_droits_afficher, " Type : ", type(data_droits_afficher))

                # Différencier les messages.
                if not data_droits_afficher and id_droit_sel == 0:
                    flash("""La table "t_personne" est vide. !""", "warning")
                elif not data_droits_afficher and id_droit_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le film {id_droit_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données personnes et droits affichés !!", "success")

        except Exception as Exception_droits_afficher:
            code, msg = Exception_droits_afficher.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception personnes_droits_afficher : {sys.exc_info()[0]} "
                  f"{Exception_droits_afficher.args[0]} , "
                  f"{Exception_droits_afficher}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template("droits/personnes_droits_afficher.html", data=data_droits_afficher)


"""
    nom: edit_droit_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "personnes_droits_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes

"""


@obj_mon_application.route("/edit_droit_selected", methods=['GET', 'POST'])
def edit_droit_selected():
    if request.method == "GET":
        try:
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_droits_afficher = """SELECT id_droit, droit FROM t_droit ORDER BY id_droit ASC"""
                mc_afficher.execute(strsql_droits_afficher)
            data_droits_all = mc_afficher.fetchall()
            print("dans edit_droit_selected ---> data_droits_all", data_droits_all)

            # Récupère la valeur de "id_film" du formulaire html "personnes_droits_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_genres_edit_html" dans le fichier "personnes_droits_afficher.html"
            # href="{{ url_for('edit_genre_film_selected', id_film_genres_edit_html=row.id_film) }}"
            id_droits_edit = request.values['id_droits_edit_html']

            # Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_droits_edit'] = id_droits_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_droit_selected_dictionnaire = {"value_id_droit_selected": id_droits_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_films_afficher_data
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_films_afficher_data"
            data_droit_selected, data_droits_non_attribues, data_droits_attribues = \
                droits_afficher_data(valeur_id_droit_selected_dictionnaire)

            print(data_droit_selected)
            lst_data_droit_selected = [item['id_film'] for item in data_droit_selected]
            print("lst_data_film_selected  ", lst_droit_selected,
                  type(lst_droit_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_droits_non_attribues = [item['id_genre'] for item in data_droits_non_attribues]
            session['session_lst_data_genres_films_non_attribues'] = lst_data_droits_non_attribues
            print("lst_data_genres_films_non_attribues  ", lst_data_droits_non_attribues,
                  type(lst_data_droits_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_droits_old_attribues = [item['id_genre'] for item in data_droits_attribues]
            session['session_lst_data_genres_films_old_attribues'] = lst_data_droits_old_attribues
            print("lst_data_genres_films_old_attribues  ", lst_data_droits_old_attribues,
                  type(lst_data_droits_old_attribues))

            print(" data data_genre_film_selected", data_droit_selected, "type ", type(data_droit_selected))
            print(" data data_genres_films_non_attribues ", data_droits_non_attribues, "type ",
                  type(data_droits_non_attribues))
            print(" data_genres_films_attribues ", data_droits_attribues, "type ",
                  type(data_droits_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "droit"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_droits_non_attribues = [item['droit'] for item in data_droits_non_attribues]
            print("lst_all_genres gf_edit_genre_film_selected ", lst_data_droits_non_attribues,
                  type(lst_data_droits_non_attribues))

        except Exception as Exception_edit_droit_selected:
            code, msg = Exception_edit_droit_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception edit_droit_selected : {sys.exc_info()[0]} "
                  f"{Exception_edit_droit_selected.args[0]} , "
                  f"{Exception_edit_droit_selected}", "danger")

    return render_template("droits/droits_modifier_tags_dropbox.html",
                           data_droits=data_droits_all,
                           data_personne_selected=data_droit_selected,
                           data_droits_attribues=data_droits_attribues,
                           data_droits_non_attribues=data_droits_non_attribues)


"""
    nom: update_genre_film_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "personnes_droits_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@obj_mon_application.route("/update_genre_film_selected", methods=['GET', 'POST'])
def update_droit_personne_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_film_selected = session['session_id_droits_edit']
            print("session['session_id_droits_edit'] ", session['session_id_droits_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_droits_non_attribues = session['session_lst_data_droits_non_attribues']
            print("old_lst_data_droits_non_attribues ", old_lst_data_droits_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_droits_attribues = session['session_lst_data_droits_old_attribues']
            print("old_lst_data_droits_old_attribues ", old_lst_data_droits_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_films_modifier_tags_dropbox.html"
            new_lst_str_droits = request.form.getlist('name_select_tags')
            print("new_lst_str_droits ", new_lst_str_droits)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_droit_old = list(map(int, new_lst_str_droits))
            print("new_lst_droit ", new_lst_int_droit_old, "type new_lst_droit ",
                  type(new_lst_int_droit_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_genre_film".
            lst_diff_droits_delete_b = list(
                set(old_lst_data_droits_attribues) - set(new_lst_int_droit_old))
            print("lst_diff_droits_delete_b ", lst_diff_droits_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_genre_film"
            lst_diff_droits_insert_a = list(
                set(new_lst_int_droit_old) - set(old_lst_data_droits_attribues))
            print("lst_diff_droits_insert_a ", lst_diff_droits_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_film" et "fk_genre"/"id_genre" dans la "t_genre_film"
            strsql_insert_droit = """INSERT INTO t_genre_film (id_genre_film, fk_genre, fk_film)
                                                    VALUES (NULL, %(value_fk_genre)s, %(value_fk_film)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_film" et "id_genre" dans la "t_genre_film"
            strsql_delete_genre_film = """DELETE FROM t_avoir_droit WHERE fk_droit = %(value_fk_droit)s AND fk_personne = %(value_fk_personne)s"""

            with MaBaseDeDonnee() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_droit_ins in lst_diff_droits_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_personne_sel_droit_sel_dictionnaire = {"value_fk_film": id_personne_selected,
                                                               "value_fk_droit": id_droit_ins}

                    mconn_bd.mabd_execute(strsql_insert_droit_film, valeurs_personne_sel_droit_sel_dictionnaire)

                # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_droit_del in lst_diff_droits_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_personne_sel_droit_sel_dictionnaire = {"value_fk_persone": id_personne_selected,
                                                               "value_fk_droit": id_droit_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.mabd_execute(strsql_delete_droit_personne, valeurs_personne_sel_droit_sel_dictionnaire)

        except Exception as Exception_update_droit_personne_selected:
            code, msg = Exception_update_droit_personne_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception update_genre_film_selected : {sys.exc_info()[0]} "
                  f"{Exception_update_droit_personne_selected.args[0]} , "
                  f"{Exception_update_droit_personne_selected}", "danger")

    # Après cette mise à jour de la table intermédiaire "t_genre_film",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('personnes_droits_afficher', id_personne_sel=id_personne_selected))


"""
    nom: genres_films_afficher_data

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "personnes_droits_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def droits_personnes_afficher_data(valeur_id_personne_selected_dict):
    print("valeur_id_personne_selected_dict...", valeur_id_personne_selected_dict)
    try:

        strsql_personne_selected = """SELECT id_personne, Nom_personne, Prenom_personne, Date_naissance_personne, Adresse_mail_personne, MDP_personne, GROUP_CONCAT(id_droit) as DroitsPersonnes FROM t_avoir_droit
                                        INNER JOIN t_personne ON t_personne.id_personne = t_avoir_droit.fk_personne
                                        INNER JOIN t_droit ON t_droit.id_droit = t_avoir_personne.fk_droit
                                        WHERE id_personne = %(value_id_personne_selected)s"""

        strsql_droits_personnes_non_attribues = """SELECT id_droit, droit FROM t_droit WHERE id_droit not in(SELECT id_droit as idDroitsPersonnes FROM t_avoir_droit
                                                    INNER JOIN t_personne ON t_personne.id_personne = t_avoir_droit.fk_personne
                                                    INNER JOIN t_droit ON t_droit.id_droit = t_avoir_droit.fk_droit
                                                    WHERE id_film = %(value_id_film_selected)s)"""

        strsql_droits_personnes_attribues = """SELECT id_personne, id_droit, droit FROM t_avoir_droit
                                            INNER JOIN t_personne ON t_personne.id_personne = t_avoir_droit.fk_personne
                                            INNER JOIN t_personne ON t_personne.id_personne = t_avoir_droit.fk_droit
                                            WHERE id_personne = %(value_id_personne_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_droits_personnes_non_attribues, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_droits_personnes_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_films_afficher_data ----> data_droits_personnes_non_attribues ", data_droits_personnes_non_attribues,
                  " Type : ",
                  type(data_droits_personnes_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_personne_selected, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_personne_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_film_selected  ", data_personne_selected, " Type : ", type(data_personne_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_droits_personnes_attribues, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_droits_personnes_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_droits_personnes_attribues ", data_droits_personnes_attribues, " Type : ",
                  type(data_droits_personnes_attribues))

            # Retourne les données des "SELECT"
            return data_personne_selected, data_droits_personnes_non_attribues, data_droits_personnes_attribues
    except pymysql.Error as pymysql_erreur:
        code, msg = pymysql_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.Error Erreur dans droits_personnes_afficher_data : {sys.exc_info()[0]} "
              f"{pymysql_erreur.args[0]} , "
              f"{pymysql_erreur}", "danger")
    except Exception as exception_erreur:
        code, msg = exception_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"Exception Erreur dans droits_personnes_afficher_data : {sys.exc_info()[0]} "
              f"{exception_erreur.args[0]} , "
              f"{exception_erreur}", "danger")
    except pymysql.err.IntegrityError as IntegrityError_droits_personnes_afficher_data:
        code, msg = IntegrityError_droits_personnes_afficher_data.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.err.IntegrityError Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{IntegrityError_droits_personnes_afficher_data.args[0]} , "
              f"{IntegrityError_droits_personnes_afficher_data}", "danger")
